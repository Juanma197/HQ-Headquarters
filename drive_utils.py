import os
import json
import shutil
import pandas as pd
from datetime import datetime
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

BASE_FOLDER = "AccountingHQ"
CATEGORIES = ["Income", "Expenses", "Invoices", "Backups", "Exports"]

def connect_to_drive():
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.txt")
    if gauth.credentials is None:
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        gauth.Refresh()
    else:
        gauth.Authorize()
    gauth.SaveCredentialsFile("mycreds.txt")
    return GoogleDrive(gauth)

def get_or_create_folder(drive, parent_id, name):
    file_list = drive.ListFile({
        'q': f"'{parent_id}' in parents and title='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    }).GetList()
    if file_list:
        return file_list[0]['id']
    folder = drive.CreateFile({
        'title': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [{'id': parent_id}]
    })
    folder.Upload()
    return folder['id']

def get_root_folder_id(drive):
    root_list = drive.ListFile({
        'q': f"title='{BASE_FOLDER}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    }).GetList()
    if root_list:
        return root_list[0]['id']
    folder = drive.CreateFile({
        'title': BASE_FOLDER,
        'mimeType': 'application/vnd.google-apps.folder'
    })
    folder.Upload()
    return folder['id']

def ensure_property_structure(drive, property_name):
    root_id = get_root_folder_id(drive)
    prop_id = get_or_create_folder(drive, root_id, property_name)

    folder_ids = {}
    for cat in CATEGORIES:
        folder_ids[cat] = get_or_create_folder(drive, prop_id, cat)

    # Also prepare subfolders for monthly/yearly structure
    month = datetime.now().strftime("%Y-%m")
    for cat in ["Income", "Expenses", "Invoices"]:
        get_or_create_folder(drive, folder_ids[cat], month)

    return folder_ids

def upload_file_to_drive(drive, parent_id, local_path, filename=None):
    file = drive.CreateFile({'parents': [{'id': parent_id}]})
    file['title'] = filename or os.path.basename(local_path)
    file.SetContentFile(local_path)
    file.Upload()

def list_files(drive, folder_id):
    return drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()

def download_file(drive, file_id, destination):
    file = drive.CreateFile({'id': file_id})
    file.GetContentFile(destination)

def backup_locally(local_path):
    local_backup = os.path.join("local_backups", os.path.basename(local_path))
    os.makedirs("local_backups", exist_ok=True)
    shutil.copy(local_path, local_backup)

def autosave_data_to_drive(drive, category, property_name, data):
    folder_ids = ensure_property_structure(drive, property_name)
    now = datetime.now()
    month = now.strftime("%Y-%m")
    filename = f"{month}.csv"
    
    if data and isinstance(data, list) and len(data) > 0:
        df = pd.DataFrame(data)
        with open(filename, "w", encoding="utf-8", newline="") as f:
            df.to_csv(f, index=False)
        month_folder_id = get_or_create_folder(drive, folder_ids[category], month)
        upload_file_to_drive(drive, month_folder_id, filename)
        backup_locally(filename)
        os.remove(filename)

def archive_old_entries(session_state, key, cutoff_date):
    if key not in session_state:
        return
    items = session_state[key]
    keep = []
    archive = []

    for entry in items:
        entry_date = entry.get("Date")
        if isinstance(entry_date, str):
            entry_date = datetime.strptime(entry_date, "%Y-%m-%d")
        if entry_date and entry_date >= cutoff_date:
            keep.append(entry)
        else:
            archive.append(entry)

    session_state[key] = keep
    return archive

def export_summary_to_drive(drive, property_name, category, data, mode="Yearly"):
    folder_ids = ensure_property_structure(drive, property_name)
    export_root = folder_ids["Exports"]

    now = datetime.now()
    period = {
        "Monthly": now.strftime("%Y-%m"),
        "Quarterly": f"{now.year}-Q{((now.month-1)//3)+1}",
        "Half-Year": f"{now.year}-H1" if now.month <= 6 else f"{now.year}-H2",
        "Yearly": f"{now.year}-{now.year+1}"
    }.get(mode, now.strftime("%Y-%m"))

    export_folder = get_or_create_folder(drive, export_root, period)
    filename = f"{category}_{period}.csv"

    if data and isinstance(data, pd.DataFrame) and not data.empty:
        data.to_csv(filename, index=False)
        upload_file_to_drive(drive, export_folder, filename)
        backup_locally(filename)
        os.remove(filename)
