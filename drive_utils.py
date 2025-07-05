import os
import json
import tempfile
from datetime import datetime
from oauth2client.service_account import ServiceAccountCredentials
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import streamlit as st

@st.cache_resource
def connect_to_drive():
    scope = ['https://www.googleapis.com/auth/drive']
    credentials_dict = dict(st.secrets["gdrive_service_account"])
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)
    gauth = GoogleAuth()
    gauth.credentials = credentials
    drive = GoogleDrive(gauth)
    return drive

def get_or_create_folder(drive, name, parent_id=None):
    query = f"title='{name}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    folders = drive.ListFile({'q': query}).GetList()
    if folders:
        return folders[0]['id']
    metadata = {'title': name, 'mimeType': 'application/vnd.google-apps.folder'}
    if parent_id:
        metadata['parents'] = [{'id': parent_id}]
    folder = drive.CreateFile(metadata)
    folder.Upload()
    return folder['id']

def ensure_property_structure(drive, property_name):
    month = datetime.today().strftime("%Y-%m")
    base_id = get_or_create_folder(drive, "AccountingHQ")
    prop_id = get_or_create_folder(drive, property_name, base_id)

    folder_ids = {}
    for sub in ["Income", "Expenses", "Invoices", "Salary", "Backups"]:
        sub_id = get_or_create_folder(drive, sub, prop_id)
        month_id = get_or_create_folder(drive, month, sub_id)
        folder_ids[sub] = month_id
    return folder_ids

def upload_file_to_drive(drive, folder_id, local_path, filename=None):
    if not filename:
        filename = os.path.basename(local_path)
    file_drive = drive.CreateFile({'title': filename, 'parents': [{'id': folder_id}]})
    file_drive.SetContentFile(local_path)
    file_drive.Upload()
    return file_drive['id']

def list_files(drive, folder_id):
    query = f"'{folder_id}' in parents and trashed=false"
    return drive.ListFile({'q': query}).GetList()

def download_file(drive, file_id, local_path):
    file_drive = drive.CreateFile({'id': file_id})
    file_drive.GetContentFile(local_path)

def backup_locally(local_path, backup_folder="backups"):
    os.makedirs(backup_folder, exist_ok=True)
    base = os.path.basename(local_path)
    dst = os.path.join(backup_folder, base)
    with open(local_path, 'rb') as src_file:
        with open(dst, 'wb') as dst_file:
            dst_file.write(src_file.read())
    return dst

def delete_property_folder(drive, property_name):
    base_id = get_or_create_folder(drive, "AccountingHQ")
    query = (
        f"title='{property_name}' and mimeType='application/vnd.google-apps.folder' "
        f"and trashed=false and '{base_id}' in parents"
    )
    results = drive.ListFile({'q': query}).GetList()
    if results:
        folder = results[0]
        folder['trashed'] = True
        folder.Upload()
