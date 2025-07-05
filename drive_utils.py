from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import streamlit as st

@st.cache_resource
def connect_to_drive():
    gauth = GoogleAuth()

    # Automatically loads settings.yaml and client_secrets.json if present
    gauth.LocalWebserverAuth()  # Opens browser login for first-time auth
    return GoogleDrive(gauth)
