import streamlit as st
import json, os
from datetime import date, datetime
from dateutil.parser import parse
from utils_drive import upload_to_drive, ensure_folder_path

st.set_page_config(page_title="⚙️ Settings & Backup", layout="centered")
st.title("⚙️ Settings & Data Backup")

if 'properties' not in st.session_state:
    st.session_state.properties = []

st.subheader("🗂️ Choose Property for Backup")
property_name = st.selectbox("Select Property", st.session_state.properties or ["No properties found"])

st.subheader("📤 Backup Notes or Upload File")
tab1, tab2 = st.tabs(["📝 Manual Note", "📁 Upload File"])

with tab1:
    note = st.text_area("Enter a note or reminder to back up")
    if st.button("📤 Upload Note to Drive"):
        if property_name and note.strip():
            today = datetime.today().strftime("%Y-%m")
            local_file = f"backups/{property_name}_{today}_note.txt"
            os.makedirs("backups", exist_ok=True)
            with open(local_file, "w") as f:
                f.write(note)
            drive_path = f"AccountingHQ/{property_name}/Backups/{today}/"
            upload_to_drive(drive_path, local_file)
            st.success("Note uploaded to Drive and backed up locally.")

with tab2:
    uploaded_file = st.file_uploader("Upload backup or contract file")
    if uploaded_file and st.button("📤 Upload File to Drive"):
        today = datetime.today().strftime("%Y-%m")
        local_path = f"backups/{uploaded_file.name}"
        with open(local_path, "wb") as f:
            f.write(uploaded_file.read())
        drive_path = f"AccountingHQ/{property_name}/Backups/{today}/"
        upload_to_drive(drive_path, local_path)
        st.success("File uploaded to Drive and saved locally.")
