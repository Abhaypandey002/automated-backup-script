# 🔐 Automated Backup and Rotation Script with Google Drive Integration

## 📘 Overview

This script automates the process of:
- Creating timestamped backups of your project folder
- Uploading backups to Google Drive using `rclone`
- Applying a professional **rotational backup strategy** (daily, weekly, monthly)
- Deleting old backups securely
- Sending success/failure **notifications** via `cURL` webhook

---

## ⚙️ Requirements

- Python 3.8+
- rclone (for Google Drive integration)
- Python packages: `python-dotenv`, `requests`

---

## 📁 Folder Structure



2. ☁️ Install and Configure rclone (for Google Drive)

🔹 Install rclone:

curl https://rclone.org/install.sh | sudo bash



Configure Google Drive:

rclone config

Type n to create a new remote

Name it (e.g., gdrive)

Choose storage: drive

Say Yes to auto config

Login in the browser

Done!


🔹 Test Upload:

rclone ls gdrive:




3. 📝 Create Your .env File

# Project Info
PROJECT_NAME=MyAwesomeApp
PROJECT_FOLDER=/full/path/to/your/project

# Backup Rotation Policy
RETENTION_DAYS=7
RETENTION_WEEKS=4
RETENTION_MONTHS=3

# Google Drive Upload
RCLONE_REMOTE=gdrive
RCLONE_FOLDER=Backups

# Webhook Notification
CURL_ENABLED=True
WEBHOOK_URL=https://webhook.site/your-unique-url



🚀 Running the Script
python backup.py



Example cURL Notification Payload

{
  "project": "MyAwesomeApp",
  "date": "2025-07-10 12:30:01",
  "test": "BackupSuccessful"
}
