import streamlit as st
import tempfile
from datetime import datetime
from drive_utils import connect_to_drive, ensure_property_structure, upload_file_to_drive, backup_locally

st.set_page_config(page_title="📥 Income Tracker", layout="centered")
st.title("📥 Upload Income Document")

drive = connect_to_drive()
st.success("✅ Connected to Google Drive")

# --- Property Selection ---
property_name = st.selectbox("🏠 Select Property", ["Example House 1", "Example House 2", "Add New..."])
if property_name == "Add New...":
    property_name = st.text_input("Enter new property name")
    if not property_name:
        st.stop()

folder_ids = ensure_property_structure(drive, property_name)
month_folder_id = folder_ids["Income"]

# --- Upload Typed Entry ---
st.subheader("📝 Enter Income Details Manually")
date = st.date_input("Date", datetime.today())
amount = st.number_input("Amount", min_value=0.0, step=0.01)
description = st.text_input("Description")
save_entry = st.button("💾 Save Entry")

if save_entry:
    content = f"Date: {date}\nAmount: {amount}\nDescription: {description}"
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w") as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    file_id = upload_file_to_drive(drive, month_folder_id, tmp_path)
    backup_locally(tmp_path)
    st.success(f"✅ Entry uploaded to Drive (ID: {file_id}) and saved locally.")

# --- Upload File ---
st.subheader("📎 Upload Document")
uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    file_id = upload_file_to_drive(drive, month_folder_id, tmp_path, uploaded_file.name)
    backup_locally(tmp_path)
    st.success(f"✅ File uploaded to Drive (ID: {file_id}) and saved locally.")
