import streamlit as st
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import json
import os

@st.cache_resource
def connect_to_drive():
    client_config = {
        "installed": {
            "client_id": st.secrets["google_oauth"]["client_id"],
            "client_secret": st.secrets["google_oauth"]["client_secret"],
            "redirect_uris": ["http://localhost"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token"
        }
    }

    temp_path = "temp_client_secrets.json"
    with open(temp_path, "w") as f:
        json.dump(client_config, f)

    gauth = GoogleAuth()
    gauth.LoadClientConfigFile(temp_path)
    gauth.CommandLineAuth()  # <-- This works on Streamlit Cloud
    os.remove(temp_path)

    return GoogleDrive(gauth)
