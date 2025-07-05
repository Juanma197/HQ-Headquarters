import streamlit as st
from drive_utils import connect_to_drive, ensure_property_structure, upload_file_to_drive, backup_locally
from datetime import datetime
import os

st.set_page_config(page_title="👤 Salary & Dividends", layout="centered")
st.title("👤 Salary and Dividend Tracker")

# Connect to Google Drive
drive = connect_to_drive()
st.success("✅ Connected to Google Drive")

# Property selection
property_name = st.selectbox("🏠 Select Property", ["Example House 1", "Example House 2", "Add New..."])
if property_name == "Add New...":
    property_name = st.text_input("Enter New Property Name")
    if not property_name:
        st.stop()

# Ensure folder structure exists
folder_ids = ensure_property_structure(drive, property_name)
month = datetime.today().strftime("%Y-%m")

# --- Upload Salary File ---
st.subheader("📤 Upload Salary Document")
salary_file = st.file_uploader("Upload Salary Slip or Record", type=["pdf", "csv", "xlsx"])
if salary_file:
    temp_path = os.path.join("temp_salary_" + salary_file.name)
    with open(temp_path, "wb") as f:
        f.write(salary_file.read())
    upload_file_to_drive(drive, folder_ids["Salary"], temp_path)
    backup_locally(temp_path)
    st.success(f"✅ '{salary_file.name}' uploaded to Salary folder and backed up locally")

# --- Enter Salary Data ---
st.subheader("📝 Typed Salary Entry")
name = st.text_input("Employee Name")
amount = st.number_input("Salary Amount", min_value=0.0, format="%.2f")
if st.button("Save Salary Record") and name:
    content = f"Date: {datetime.today().strftime('%Y-%m-%d')}\nName: {name}\nAmount: £{amount:.2f}"
    local_txt_path = f"salary_{name.replace(' ', '_')}_{datetime.today().strftime('%Y%m%d')}.txt"
    with open(local_txt_path, "w") as f:
        f.write(content)
    upload_file_to_drive(drive, folder_ids["Salary"], local_txt_path)
    backup_locally(local_txt_path)
    st.success("✅ Salary entry saved and uploaded")

# --- Upload Dividend File ---
st.subheader("📤 Upload Dividend Document")
dividend_file = st.file_uploader("Upload Dividend Voucher or Record", type=["pdf", "csv", "xlsx"], key="div")
if dividend_file:
    temp_path = os.path.join("temp_dividend_" + dividend_file.name)
    with open(temp_path, "wb") as f:
        f.write(dividend_file.read())
    upload_file_to_drive(drive, folder_ids["Salary"], temp_path)
    backup_locally(temp_path)
    st.success(f"✅ '{dividend_file.name}' uploaded to Salary folder and backed up locally")

# --- Enter Dividend Data ---
st.subheader("📝 Typed Dividend Entry")
shareholder = st.text_input("Shareholder Name")
dividend_amount = st.number_input("Dividend Amount", min_value=0.0, format="%.2f")
if st.button("Save Dividend Record") and shareholder:
    content = f"Date: {datetime.today().strftime('%Y-%m-%d')}\nShareholder: {shareholder}\nDividend: £{dividend_amount:.2f}"
    local_txt_path = f"dividend_{shareholder.replace(' ', '_')}_{datetime.today().strftime('%Y%m%d')}.txt"
    with open(local_txt_path, "w") as f:
        f.write(content)
    upload_file_to_drive(drive, folder_ids["Salary"], local_txt_path)
    backup_locally(local_txt_path)
    st.success("✅ Dividend entry saved and uploaded")

