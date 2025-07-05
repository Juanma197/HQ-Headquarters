import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

@st.cache_resource
def connect_to_drive():
    scope = ['https://www.googleapis.com/auth/drive']
    credentials_dict = dict(st.secrets["gdrive_service_account"])

    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)

    gauth = GoogleAuth()
    gauth.credentials = credentials

    # ❌ Don't call LoadServiceConfigSettings() unless you use settings.yaml
    # gauth.LoadServiceConfigSettings()

    drive = GoogleDrive(gauth)
    return drive
