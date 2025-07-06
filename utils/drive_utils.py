# utils/drive_utils.py

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
from datetime import datetime
import tempfile
import shutil

# 1. Connect to Google Drive
def connect_to_drive():
    gauth = GoogleAuth()
    gauth.LocalWebserverAuth()  # This opens a browser window to authenticate
    return GoogleDrive(gauth)

# 2. Create or retrieve folder ID by name
def get_or_create_folder(drive, parent_id, folder_name):
    query = f"'{parent_id}' in parents and title = '{folder_name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    file_list = drive.ListFile({'q': query}).GetList()
    if file_list:
        return file_list[0]['id']
    folder_metadata = {
        'title': folder_name,
        'parents': [{'id': parent_id}],
        'mimeType': 'application/vnd.google-apps.folder'
    }
    folder = drive.CreateFile(folder_metadata)
    folder.Upload()
    return folder['id']

# 3. Ensure full folder structure for a property
def ensure_property_structure(drive, property_name):
    base_folder_id = get_or_create_folder(drive, 'root', 'AccountingHQ')

    subfolders = ['Income', 'Expenses', 'Invoices', 'Salary', 'Dividends', 'Settings', 'Backups', 'Exports']
    folder_ids = {}

    # Create or get main property folder
    property_folder_id = get_or_create_folder(drive, base_folder_id, property_name)

    # Create subfolders
    for name in subfolders:
        folder_ids[name] = get_or_create_folder(drive, property_folder_id, name)

    return folder_ids  # e.g., folder_ids["Income"] = <ID>

# 4. Upload a file to Drive
def upload_file_to_drive(drive, folder_id, file_path, filename=None):
    if filename is None:
        filename = os.path.basename(file_path)
    gfile = drive.CreateFile({'title': filename, 'parents': [{'id': folder_id}]})
    gfile.SetContentFile(file_path)
    gfile.Upload()
    return gfile['id']

# 5. Backup locally in a dated /Backups folder
def backup_locally(file_path):
    today = datetime.now().strftime("%Y-%m-%d")
    backup_dir = os.path.join("Backups", today)
    os.makedirs(backup_dir, exist_ok=True)
    shutil.copy(file_path, os.path.join(backup_dir, os.path.basename(file_path)))

# 6. Delete file from a Drive folder by name
def delete_file_from_drive(drive, folder_id, filename):
    query = f"'{folder_id}' in parents and title = '{filename}' and trashed = false"
    file_list = drive.ListFile({'q': query}).GetList()
    for f in file_list:
        f.Delete()
