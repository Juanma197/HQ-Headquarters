def get_or_create_folder(drive, parent_folder_id, folder_name):
    query = f"'{parent_folder_id}' in parents and trashed=false and title='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
    file_list = drive.ListFile({'q': query}).GetList()
    if file_list:
        return file_list[0]['id']
    else:
        folder_metadata = {
            'title': folder_name,
            'mimeType': 'application/vnd.google-apps.folder',
            'parents': [{'id': parent_folder_id}]
        }
        folder = drive.CreateFile(folder_metadata)
        folder.Upload()
        return folder['id']


def upload_file_to_drive(folder_id, local_file_path, new_filename=None):
    file_drive = drive.CreateFile({'parents': [{'id': folder_id}]})
    file_drive['title'] = new_filename or os.path.basename(local_file_path)
    file_drive.SetContentFile(local_file_path)
    file_drive.Upload()
    return file_drive['id']


def list_files(folder_id):
    query = f"'{folder_id}' in parents and trashed=false"
    return drive.ListFile({'q': query}).GetList()


def download_file(file_id, save_path):
    file = drive.CreateFile({'id': file_id})
    file.GetContentFile(save_path)
