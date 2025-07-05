import streamlit as st
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import json
import tempfile

@st.cache_resource
def connect_to_drive():
    # Extract service account credentials from Streamlit secrets
    credentials_dict = dict(st.secrets["gdrive_service_account"])

    # Write credentials to a temporary JSON file
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".json", delete=False) as temp_file:
        json.dump(credentials_dict, temp_file)
        temp_file.flush()

        # Authenticate with PyDrive2 using the temporary file
        gauth = GoogleAuth()
        gauth.LoadServiceConfigSettings()  # optional: load settings.yaml if using
        gauth.LoadCredentialsFile(temp_file.name)
        gauth.ServiceAuth()

    return GoogleDrive(gauth)
