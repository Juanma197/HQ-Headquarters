import json
import tempfile
from oauth2client.service_account import ServiceAccountCredentials
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import streamlit as st

@st.cache_resource
def connect_to_drive():
    scope = ['https://www.googleapis.com/auth/drive']
    credentials_dict = dict(st.secrets["gdrive_service_account"])

    # Create credentials object from secrets
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)

    # Authorize with PyDrive2
    gauth = GoogleAuth()
    gauth.credentials = credentials
    drive = GoogleDrive(gauth)

    return drive
