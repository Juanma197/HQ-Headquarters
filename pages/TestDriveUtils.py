import streamlit as st
from utils.drive_utils import connect_to_drive

st.title("Test Drive Connection")

try:
    drive = connect_to_drive()
    st.success("✅ Drive connection successful.")
except Exception as e:
    st.error(f"❌ Error connecting to drive: {e}")
