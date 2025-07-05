import os
import streamlit as st
from drive_utils import connect_to_drive, list_files, download_file
from datetime import datetime
import zipfile
import io

st.set_page_config(page_title="📤 Export Centre", layout="wide")
st.title("📤 Export Centre")

drive = connect_to_drive()

property_name = st.selectbox("🏠 Select Property", ["Example House 1", "Example House 2"])
category = st.selectbox("📂 Select Category", ["Income", "Expenses", "Invoices", "Salary", "Backups"])
month = st.selectbox("🗓️ Select Month", [datetime.today().strftime("%Y-%m")])

folder_structure = f"AccountingHQ/{property_name}/{category}/{month}"

# Get folder ID recursively
def get_folder_id_by_path(path_parts):
    parent_id = None
    for part in path_parts:
        parent_id = get_or_create_folder(drive, part, parent_id)
    return parent_id

from drive_utils import get_or_create_folder

folder_id = get_folder_id_by_path(folder_structure.split("/"))
files = list_files(drive, folder_id)

st.subheader("📄 Files")
if not files:
    st.info("No files found in the selected folder.")
else:
    for file in files:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{file['title']}**")
        with col2:
            with open(f"temp_{file['title']}", "wb") as f:
                file.GetContentFile(f.name)
                with open(f.name, "rb") as f_read:
                    st.download_button("⬇️ Download", f_read.read(), file_name=file['title'])

    if st.button("📦 Download All as ZIP"):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zf:
            for file in files:
                file_path = f"temp_{file['title']}"
                file.GetContentFile(file_path)
                zf.write(file_path, arcname=file['title'])
        zip_buffer.seek(0)
        st.download_button("⬇️ Download ZIP", zip_buffer.read(), file_name=f"{property_name}_{category}_{month}.zip")
