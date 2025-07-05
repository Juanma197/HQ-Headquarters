import json
import tempfile
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import streamlit as st  # ✅ make sure this line is ABOVE the decorator

@st.cache_resource
def connect_to_drive():
    gauth = GoogleAuth()

    # For Streamlit secrets dict to JSON serializable format
    credentials_dict = dict(st.secrets["gdrive_service_account"])

    # Option 1: use LoadServiceConfigFile if available (preferred)
    with tempfile.NamedTemporaryFile(mode="w+", delete=False) as temp_file:
        json.dump(credentials_dict, temp_file)
        temp_file.flush()
        gauth.LoadServiceConfigFile(temp_file.name)

    gauth.ServiceAuth()
    return GoogleDrive(gauth)
