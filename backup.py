import os
import zipfile
from datetime import datetime
from dotenv import load_dotenv
import logging
import subprocess
import requests

# Load environment variables from .env file
load_dotenv()

# Get values from .env
PROJECT_NAME = os.getenv("PROJECT_NAME")
PROJECT_FOLDER = os.getenv("PROJECT_FOLDER")
BACKUP_DIR = os.path.join("backups", "daily")

# Setup logging
LOG_DIR = "backup_logs"
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    filename=os.path.join(LOG_DIR, f"{datetime.now().date()}.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Ensure backup folder exists
os.makedirs(BACKUP_DIR, exist_ok=True)


RCLONE_REMOTE = os.getenv("RCLONE_REMOTE")
RCLONE_FOLDER = os.getenv("RCLONE_FOLDER")

def upload_to_gdrive(zip_file_path):
    try:
        if not os.path.exists(zip_file_path):
            logging.error(f"Backup file not found: {zip_file_path}")
            print(f"[✗] Cannot upload. File not found.")
            return False

        # Compose rclone command
        rclone_path = f"{RCLONE_REMOTE}:{RCLONE_FOLDER}"
        command = ["rclone", "copy", zip_file_path, rclone_path]

        # Run rclone
        subprocess.run(command, check=True)

        logging.info(f"Backup uploaded to Google Drive: {rclone_path}")
        print(f"[✓] Backup uploaded to Google Drive: {rclone_path}")
        return True

    except subprocess.CalledProcessError as e:
        logging.error(f"rclone failed: {e}")
        print(f"[✗] Upload failed: {e}")
        return False

def create_zip_backup():
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        zip_filename = f"{PROJECT_NAME}_{timestamp}.zip"
        zip_filepath = os.path.join(BACKUP_DIR, zip_filename)

        # Create the zip file
        with zipfile.ZipFile(zip_filepath, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, _, files in os.walk(PROJECT_FOLDER):
                for file in files:
                    filepath = os.path.join(root, file)
                    arcname = os.path.relpath(filepath, PROJECT_FOLDER)
                    zipf.write(filepath, arcname)

        logging.info(f"Backup created successfully: {zip_filepath}")
        print(f"[✓] Backup created: {zip_filepath}")
        return zip_filepath

    except Exception as e:
        logging.error(f"Backup failed: {e}")
        print(f"[✗] Backup failed: {e}")
        return None

# Determine Type of Backup (daily/weekly/monthly)
def get_backup_type():
    today = datetime.now()
    if today.day == 1:
        return "monthly"
    elif today.weekday() == 6:  # Sunday
        return "weekly"
    else:
        return "daily"

# Move Backup ZIP to Correct Folder
def move_backup_to_type_folder(zip_file_path, backup_type):
    dest_dir = os.path.join("backups", backup_type)
    os.makedirs(dest_dir, exist_ok=True)

    filename = os.path.basename(zip_file_path)
    dest_path = os.path.join(dest_dir, filename)

    os.rename(zip_file_path, dest_path)

    logging.info(f"Moved backup to {backup_type}: {dest_path}")
    print(f"[✓] Backup categorized under '{backup_type}'")
    return dest_path

# Clean Up Old Backups
def clean_old_backups(backup_type, keep_count):
    folder = os.path.join("backups", backup_type)
    if not os.path.exists(folder):
        return

    files = sorted(
        [os.path.join(folder, f) for f in os.listdir(folder)],
        key=os.path.getmtime,
        reverse=True
    )

    # Keep only the latest 'keep_count' files
    for old_file in files[keep_count:]:
        try:
            os.remove(old_file)
            logging.info(f"Deleted old {backup_type} backup: {old_file}")
            print(f"[i] Deleted old {backup_type} backup: {old_file}")
        except Exception as e:
            logging.error(f"Failed to delete old backup {old_file}: {e}")

# send_curl_notification
def send_curl_notification(success=True):
    curl_enabled = os.getenv("CURL_ENABLED", "False").lower() == "true"
    webhook_url = os.getenv("WEBHOOK_URL")

    if not curl_enabled:
        print("[i] CURL notifications are disabled in .env")
        return

    if not webhook_url:
        logging.warning("CURL notification skipped: WEBHOOK_URL not set")
        return

    payload = {
        "project": PROJECT_NAME,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "test": "BackupSuccessful" if success else "BackupFailed"
    }

    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        if response.status_code == 200:
            logging.info("cURL Notification sent successfully")
            print("[✓] Notification sent via cURL")
        else:
            logging.warning(f"Notification failed: {response.status_code} - {response.text}")
            print("[✗] Notification failed")
    except Exception as e:
        logging.error(f"Notification error: {e}")
        print(f"[✗] Notification error: {e}")


# if __name__ == "__main__":
#     zip_path = create_zip_backup()
#     if zip_path:
#         upload_to_gdrive(zip_path)


if __name__ == "__main__":
    zip_path = create_zip_backup()

    if zip_path:
        backup_type = get_backup_type()

        # Move backup to correct folder (daily/weekly/monthly)
        categorized_path = move_backup_to_type_folder(zip_path, backup_type)

        # Clean old backups
        if backup_type == "daily":
            clean_old_backups("daily", int(os.getenv("RETENTION_DAYS", 7)))
        elif backup_type == "weekly":
            clean_old_backups("weekly", int(os.getenv("RETENTION_WEEKS", 4)))
        elif backup_type == "monthly":
            clean_old_backups("monthly", int(os.getenv("RETENTION_MONTHS", 3)))

        # Upload to GDrive
        # upload_to_gdrive(categorized_path)
                # Upload to GDrive
        if upload_to_gdrive(categorized_path):
            send_curl_notification(success=True)
        else:
            send_curl_notification(success=False)

