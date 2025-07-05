import streamlit as st
from drive_utils import connect_to_drive, ensure_property_structure, list_files
from datetime import datetime

st.set_page_config(page_title="📊 Dashboard", layout="wide")
st.title("📊 View Uploaded Files by Property")

drive = connect_to_drive()
st.success("✅ Connected to Google Drive")

property_name = st.selectbox("🏠 Select Property", ["Example House 1", "Example House 2", "Add New..."])
if property_name == "Add New...":
    property_name = st.text_input("Enter new property name")
    if not property_name:
        st.stop()

folder_ids = ensure_property_structure(drive, property_name)

st.header(f"📂 Files for {property_name}")
for category, folder_id in folder_ids.items():
    st.subheader(f"📁 {category}")
    files = list_files(drive, folder_id)
    if files:
        for f in files:
            st.markdown(f"- [{f['title']}]({f['alternateLink']})")
    else:
        st.markdown("_No files found._")
