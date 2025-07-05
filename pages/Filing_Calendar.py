import streamlit as st
from datetime import datetime
import os
from drive_utils import connect_to_drive, ensure_property_structure, upload_file_to_drive, backup_locally

st.set_page_config(page_title="📅 Filing Calendar")
st.title("📅 Filing Calendar")

drive = connect_to_drive()

property_name = st.selectbox("Select Property", ["Example House 1", "Example House 2", "Add New..."])
if property_name == "Add New...":
    property_name = st.text_input("Enter New Property Name")
    if not property_name:
        st.stop()

folder_ids = ensure_property_structure(drive, property_name)
backup_folder = folder_ids["Backups"]

st.subheader("📆 Important Deadlines")
st.markdown("""
- **VAT Return Due**: 7th of every third month
- **Corporation Tax Payment**: 9 months after year end
- **Annual Accounts Filing**: 9 months after year end
""")

st.subheader("📝 Save Custom Reminder")
reminder = st.text_input("Write a quick note or reminder:")
if st.button("💾 Save Reminder"):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"reminder_{timestamp}.txt"
    local_path = os.path.join("temp", filename)
    os.makedirs("temp", exist_ok=True)
    with open(local_path, "w") as f:
        f.write(reminder)
    upload_file_to_drive(drive, backup_folder, local_path)
    backup_locally(local_path)
    st.success("✅ Reminder saved to Drive and local backup.")

