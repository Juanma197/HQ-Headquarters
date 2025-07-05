from pydrive2.auth import ServiceAccountAuth
from pydrive2.drive import GoogleDrive
import streamlit as st
import json

@st.cache_resource
def connect_to_drive():
    # Convert secrets to actual dict
    service_account_data = dict(st.secrets["gdrive_service_account"])

    # Fix newlines in private key
    service_account_data["private_key"] = service_account_data["private_key"].replace("\\n", "\n")

    # Authenticate using service account
    auth = ServiceAccountAuth()
    auth.auth_method = "service"
    auth.settings = {
        "client_config": service_account_data
    }
    auth.Authorize()

    return GoogleDrive(auth)
