import streamlit as st
from datetime import datetime
import tempfile
import pandas as pd
from drive_utils import connect_to_drive, ensure_property_structure, upload_file_to_drive, backup_locally

st.set_page_config(page_title="⚙️ Settings & Backup", layout="centered")
st.title("⚙️ Settings & Auto Backup")

# Load session state defaults
if "properties" not in st.session_state:
    st.session_state.properties = []

if "income" not in st.session_state:
    st.session_state.income = []

if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "invoices" not in st.session_state:
    st.session_state.invoices = []

# Select current property for saving
property_name = st.selectbox("Select Property", st.session_state.properties if st.session_state.properties else ["No Properties Found"])

# Setup Google Drive connection + folder structure
drive = connect_to_drive()
folder_ids = ensure_property_structure(drive, property_name)
now = datetime.now()
current_month = now.strftime("%Y-%m")

# Helper function: Save dataframe to Drive + Local
def save_and_clear_data(data, category, filename_base, session_key):
    if not data:
        return

    # Filter to keep only current month
    df = pd.DataFrame(data)
    df["Date"] = pd.to_datetime(df["Date"])
    current_df = df[df["Date"].dt.strftime("%Y-%m") == current_month]
    archive_df = df[df["Date"].dt.strftime("%Y-%m") != current_month]

    # Update session state: keep only current month
    st.session_state[session_key] = current_df.to_dict("records")

    # Save archive to Drive
    if not archive_df.empty:
        temp_csv = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        archive_df.to_csv(temp_csv.name, index=False)
        upload_file_to_drive(
            drive,
            folder_ids[category],
            temp_csv.name,
            filename=f"{filename_base}_{current_month}.csv"
        )
        backup_locally(temp_csv.name)

# Backup income, expenses, invoices
save_and_clear_data(st.session_state.income, "Income", "income_backup", "income")
save_and_clear_data(st.session_state.expenses, "Expenses", "expenses_backup", "expenses")
save_and_clear_data(st.session_state.invoices, "Invoices", "invoices_backup", "invoices")

# UI: Manual note input (optional)
st.subheader("📝 Manual Settings Note (Optional)")
note = st.text_area("Enter settings or backup notes")

if st.button("💾 Save Note"):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
        tmp_file.write(note.encode("utf-8"))
        tmp_file_path = tmp_file.name
    upload_file_to_drive(drive, folder_ids["Backups"], tmp_file_path, filename="settings_note.txt")
    backup_locally(tmp_file_path)
    st.success("Note backed up to Google Drive and locally.")

# UI: Manual file uploader (optional)
st.subheader("📤 Upload a Settings Backup File (Optional)")
uploaded = st.file_uploader("Upload file")

if uploaded and st.button("📁 Upload File"):
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(uploaded.read())
        tmp_file_path = tmp_file.name
    upload_file_to_drive(drive, folder_ids["Backups"], tmp_file_path, filename=uploaded.name)
    backup_locally(tmp_file_path)
    st.success("File uploaded to Google Drive and locally.")
