import streamlit as st
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import tempfile
import json

@st.cache_resource
def connect_to_drive():
    # Load credentials from Streamlit secrets
    credentials = st.secrets["gdrive_service_account"]

    # Write the credentials to a temporary file
    with tempfile.NamedTemporaryFile(mode="w+", delete=False, suffix=".json") as temp_file:
        json.dump(credentials, temp_file)
        temp_file.flush()

        # Authenticate using service account
        gauth = GoogleAuth()
        gauth.LoadServiceConfigFile(temp_file.name)
        gauth.ServiceAuth()

    # Connect to Google Drive
    drive = GoogleDrive(gauth)
    return drive
