import streamlit as st
from datetime import datetime
import os
from drive_utils import connect_to_drive, ensure_property_structure, upload_file_to_drive, backup_locally

st.set_page_config(page_title="⚙️ Settings & Backup")

st.title("⚙️ Settings & Backup")
drive = connect_to_drive()

property_name = st.selectbox("Select Property", ["Example House 1", "Example House 2", "Add New..."])
if property_name == "Add New...":
    property_name = st.text_input("Enter New Property Name")
    if not property_name:
        st.stop()

folder_ids = ensure_property_structure(drive, property_name)
backup_folder = folder_ids["Backups"]

st.subheader("📝 Backup Notes or Settings")

text_note = st.text_area("Write notes or settings manually:")
if st.button("💾 Save Text Note"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"settings_note_{timestamp}.txt"
    local_path = os.path.join("temp", filename)
    os.makedirs("temp", exist_ok=True)
    with open(local_path, "w") as f:
        f.write(text_note)
    upload_file_to_drive(drive, backup_folder, local_path)
    backup_locally(local_path)
    st.success("✅ Note saved to Drive and local backup.")

st.subheader("📁 Upload Backup File")
uploaded = st.file_uploader("Upload file")
if uploaded:
    temp_path = os.path.join("temp", uploaded.name)
    with open(temp_path, "wb") as f:
        f.write(uploaded.read())
    upload_file_to_drive(drive, backup_folder, temp_path)
    backup_locally(temp_path)
    st.success("✅ File uploaded to Drive and backed up locally.")
