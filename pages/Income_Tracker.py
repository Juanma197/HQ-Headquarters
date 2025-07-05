import streamlit as st
from datetime import datetime
import os
import tempfile
from drive_utils import connect_to_drive, ensure_property_structure, upload_file_to_drive, backup_locally

st.set_page_config(page_title="📥 Income Tracker", layout="centered")
st.title("📥 Income Tracker")

# Connect to Drive
drive = connect_to_drive()

# --- Property Selection ---
property_name = st.selectbox("Select Property", ["Example House 1", "Example House 2", "Add New..."])
if property_name == "Add New...":
    property_name = st.text_input("Enter New Property Name")
    if not property_name:
        st.stop()

# --- Ensure folder structure ---
folder_ids = ensure_property_structure(drive, property_name)

# --- Month Selection ---
selected_month = st.selectbox("Select Month", [datetime.today().strftime("%Y-%m")])  # Simplified for now

# --- Upload Option ---
st.subheader("📄 Upload File")
uploaded_file = st.file_uploader("Choose a file to upload")

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded_file.read())
        tmp_file_path = tmp_file.name

    st.success(f"File saved temporarily: {uploaded_file.name}")

    folder_id = folder_ids['Income']  # Already contains month layer
    uploaded_id = upload_file_to_drive(drive, folder_id, tmp_file_path, uploaded_file.name)
    backup_locally(tmp_file_path)

    st.success(f"✅ File uploaded to Google Drive (ID: {uploaded_id})")

# --- Manual Entry Option ---
st.subheader("📝 Manual Income Entry")
date = st.date_input("Date", datetime.today())
amount = st.number_input("Amount", min_value=0.0, step=0.01)
description = st.text_input("Description")
submit = st.button("Save Entry")

if submit:
    filename = f"income_{date}_{property_name.replace(' ', '_')}.txt"
    content = f"Date: {date}\nAmount: {amount}\nDescription: {description}\nProperty: {property_name}\n"

    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
        tmp_file.write(content.encode())
        tmp_file_path = tmp_file.name

    folder_id = folder_ids['Income']
    uploaded_id = upload_file_to_drive(drive, folder_id, tmp_file_path, filename)
    backup_locally(tmp_file_path)

    st.success(f"✅ Entry uploaded to Google Drive (ID: {uploaded_id})")
