from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import streamlit as st

@st.cache_resource
def connect_to_drive():
    gauth = GoogleAuth()
    gauth.LoadClientConfigFile("client_secrets.json")
    gauth.LoadSettingsFile("settings.yaml")
    gauth.LocalWebserverAuth()
    return GoogleDrive(gauth)
