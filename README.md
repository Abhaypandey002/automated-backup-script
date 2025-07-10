# Automated Backup & Rotation Script with Google Drive Integration

A powerful, automated backup script that handles:

- **Project folder backups**
- **Google Drive uploads** using `rclone`
- **Rotational backup strategy** (Daily, Weekly, Monthly)
- **Old backup pruning**
- **Webhook notifications** for success/failure

---

## Requirements

To run this script, ensure the following tools are installed:

- Python **3.8+**
- [rclone](https://rclone.org/) – for Google Drive integration
- Python packages:
  - `python-dotenv`
  - `requests`

---

## Folder Structure

  ![image](https://github.com/user-attachments/assets/6b38a0bf-cf4c-4dec-876d-89d4bdec9baf)



## Step 1: Install & Configure `rclone` for Google Drive

### 🔹 Install rclone:
[curl https://rclone.org/install.sh | sudo bash]  (https://rclone.org/install/#linux)

### 🔹 Create API Client ID and Secret:

      1.Go to the Google Cloud Console
      2.Create a new project (or use an existing one)
      3.Enable the Google Drive API in your project
      4.Go to APIs & Services → Credentials
      5.Click "Create Credentials" → "OAuth client ID"
      6.Choose Desktop App as the application type
      7.Copy the generated Client ID and Client Secret
      8.Under OAuth consent screen, add your Google account under Test Users


## Step 2: Configure rclone

### Open your terminal and run:
  - `rclone config`

### Then follow this step-by-step: 
      n) New remote
      name> gdrive-enacton
      Storage> drive
      client_id> [your client_id].apps.googleusercontent.com
      client_secret> [your_client_secret]
      scope> 1
      service_account_file> (leave blank)
      Edit advanced config? n
      Use web browser to authenticate? y


### A browser will open. Log in and allow access.

### In terminal 
1. Configure this as a Shared Drive (Team Drive)? n
2. Keep this "gdrive-enacton" remote? y


## 🧪 Step 3: Test the rclone remote
 - `rclone ls gdrive-enacton:`

## 📄 Create a .env File

### Add the following content to a .env file in your project root:
    PROJECT_FOLDER=/home/abhay/dev/project
    RETENTION_DAYS=7
    RETENTION_WEEKS=4
    RETENTION_MONTHS=3
    RCLONE_REMOTE=gdrive-enacton
    RCLONE_FOLDER=Backups
    CURL_ENABLED=True
    WEBHOOK_URL=https://webhook.site/abc


## Explanation

1. PROJECT_NAME: Will be used in backup filename
2. PROJECT_FOLDER: Path to the folder you want to back up
3. RCLONE_REMOTE: Must match the name you gave in rclone config
4. RCLONE_FOLDER: Destination folder name in your Google Drive
5. WEBHOOK_URL: Any webhook for alerting (you can use https://webhook.site)

## 🚀 Run the Backup Script
  - `python backup.py`

### This will:
1. Create a zipped backup of your project folder
2. Save it under backups/daily/
3. Upload it to Google Drive under the folder Backups/
4. Log all actions in backup_logs/YYYY-MM-DD.log
5. Send a webhook notification (if WEBHOOK_URL is set)


