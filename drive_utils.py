import json
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import streamlit as st
from oauth2client.service_account import ServiceAccountCredentials

@st.cache_resource
def connect_to_drive():
    # Load secrets from Streamlit's secrets.toml
    credentials_dict = dict(st.secrets["gdrive_service_account"])

    # Define required Drive API scope
    scope = ["https://www.googleapis.com/auth/drive"]

    # Authenticate using the service account JSON contents
    credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, scope)

    gauth = GoogleAuth()
    gauth.credentials = credentials
    return GoogleDrive(gauth)
