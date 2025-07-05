import streamlit as st
from datetime import datetime
from drive_utils import connect_to_drive, ensure_property_structure, upload_file_to_drive, backup_locally
import tempfile

st.title("⚙️ Settings & Backup")

property_name = st.selectbox("Select Property", ["Example House 1", "Example House 2"])
drive = connect_to_drive()
folder_ids = ensure_property_structure(drive, property_name)
backup_folder_id = folder_ids["Backups"]

st.subheader("🔒 Save a settings note")
note = st.text_area("Enter settings or backup notes here")

if st.button("💾 Save Note"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
        tmp_file.write(note.encode("utf-8"))
        tmp_file_path = tmp_file.name
    upload_file_to_drive(drive, backup_folder_id, tmp_file_path, filename="settings_note.txt")
    backup_locally(tmp_file_path)
    st.success("Note backed up to Google Drive and locally!")

st.subheader("📤 Upload backup file")
uploaded = st.file_uploader("Upload a settings backup file")

if uploaded and st.button("📁 Upload File"):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded.read())
        tmp_file_path = tmp_file.name
    upload_file_to_drive(drive, backup_folder_id, tmp_file_path, filename=uploaded.name)
    backup_locally(tmp_file_path)
    st.success("File uploaded to Drive and locally backed up.")
