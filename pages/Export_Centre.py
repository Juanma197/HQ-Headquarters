import streamlit as st
import os
import zipfile
from drive_utils import connect_to_drive, ensure_property_structure, list_files, download_file

st.set_page_config(page_title="📤 Export Centre", layout="wide")
st.title("📤 Export Files")

drive = connect_to_drive()

property_name = st.selectbox("🏠 Select Property", ["Example House 1", "Example House 2", "Add New..."])
if property_name == "Add New...":
    property_name = st.text_input("Enter new property name")
    if not property_name:
        st.stop()

folder_ids = ensure_property_structure(drive, property_name)

temp_dir = "temp_exports"
os.makedirs(temp_dir, exist_ok=True)

for category, folder_id in folder_ids.items():
    st.subheader(f"📁 {category}")
    files = list_files(drive, folder_id)
    if not files:
        st.markdown("_No files found._")
        continue

    for file in files:
        file_name = file['title']
        file_id = file['id']
        if st.button(f"⬇️ Download {file_name}", key=f"{category}_{file_id}"):
            local_path = os.path.join(temp_dir, file_name)
            download_file(drive, file_id, local_path)
            with open(local_path, "rb") as f:
                st.download_button(label=f"📥 Save {file_name}", data=f.read(), file_name=file_name)

# Optional ZIP download
if st.button("📦 Download All as ZIP"):
    zip_path = os.path.join(temp_dir, f"{property_name}_export.zip")
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        for category, folder_id in folder_ids.items():
            files = list_files(drive, folder_id)
            for file in files:
                local_path = os.path.join(temp_dir, file['title'])
                download_file(drive, file['id'], local_path)
                zipf.write(local_path, arcname=os.path.join(category, file['title']))
    with open(zip_path, 'rb') as f:
        st.download_button("📦 Save ZIP", data=f.read(), file_name=os.path.basename(zip_path))
