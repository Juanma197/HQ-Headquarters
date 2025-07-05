import streamlit as st
from datetime import datetime
from drive_utils import connect_to_drive, ensure_property_structure, upload_file_to_drive, backup_locally
import tempfile

st.title("📅 Filing Calendar")

property_name = st.selectbox("Select Property", ["Example House 1", "Example House 2"])
drive = connect_to_drive()
folder_ids = ensure_property_structure(drive, property_name)
backup_folder_id = folder_ids["Backups"]

st.markdown("""
### Deadlines
- 📌 VAT Submission: 7th each month
- 🧾 Corporation Tax: 9 months after year-end
- 💼 Payroll filing: Last working day monthly
""")

st.subheader("📝 Save a deadline reminder (optional)")
reminder = st.text_input("Enter reminder note (e.g. 'VAT due soon')")

if st.button("💾 Save Reminder"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
        tmp_file.write(reminder.encode("utf-8"))
        tmp_file_path = tmp_file.name
    upload_file_to_drive(drive, backup_folder_id, tmp_file_path, filename="filing_reminder.txt")
    backup_locally(tmp_file_path)
    st.success("Reminder saved to Drive and backed up.")
