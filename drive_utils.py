from oauth2client.service_account import ServiceAccountCredentials

@st.cache_resource
def connect_to_drive():
    gauth = GoogleAuth()

    credentials_dict = dict(st.secrets["gdrive_service_account"])
    scope = ['https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)

    gauth.credentials = credentials
    drive = GoogleDrive(gauth)
    return drive
