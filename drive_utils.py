import json
import tempfile
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import streamlit as st

@st.cache_resource
def connect_to_drive():
    gauth = GoogleAuth()

    # Convert secrets to JSON-compatible dict
    credentials = json.loads(json.dumps(dict(st.secrets["gdrive_service_account"])))

    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        json.dump(credentials, temp_file)
        temp_file.flush()
        gauth.LoadCredentialsFile(temp_file.name)  # ← corrected here

    gauth.ServiceAuth()
    return GoogleDrive(gauth)
