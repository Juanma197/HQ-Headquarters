import streamlit as st
import pandas as pd
from datetime import datetime
import json
import tempfile
from utils.drive_utils import (
    connect_to_drive,
    ensure_property_structure,
    upload_file_to_drive,
    delete_file_from_drive,
    backup_locally,
    create_drive_folder,
    list_files_in_folder,
    get_or_create_folder,
)



st.title("📥 Income & 💸 Expense Tracker")

if 'income' not in st.session_state:
    st.session_state.income = []
if 'expenses' not in st.session_state:
    st.session_state.expenses = []
if 'properties' not in st.session_state:
    st.session_state.properties = []

ownership_types = ["Personal", "Ltd"]
properties = st.session_state["properties"]
drive = connect_to_drive()

def add_entry(storage, entry, folder_name, property_name):
    storage.append(entry)

    # Save to Drive
    folder_ids = ensure_property_structure(drive, property_name)
    folder_id = folder_ids[folder_name]
    filename = f"{entry['Date']}_{folder_name}_{property_name}.json"
    save_path = tempfile.NamedTemporaryFile(delete=False, suffix=".json").name
    with open(save_path, "w") as f:
        json.dump(entry, f, indent=2)
    upload_file_to_drive(drive, folder_id, save_path, filename)

tab1, tab2 = st.tabs(["📥 Income", "💸 Expenses"])

with tab1:
    st.header("Log Income")
    with st.form("income_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            date = st.date_input("Date", value=datetime.today())
            amount = st.number_input("Amount (£)", min_value=0.0, step=10.0)
        with col2:
            category = st.selectbox("Category", ["Rental", "Management Fee", "Consulting"])
            property_name = st.selectbox("Property", properties if properties else ["No properties found"])
        with col3:
            ownership = st.selectbox("Ownership Type", ownership_types)
            notes = st.text_input("Notes")
        submitted = st.form_submit_button("Add Income")
        if submitted:
            entry = {
                "Date": date.strftime("%Y-%m-%d"),
                "Amount": amount,
                "Category": category,
                "Property": property_name,
                "Ownership": ownership,
                "Notes": notes
            }
            add_entry(st.session_state.income, entry, "Income", property_name)
            st.success("Income added.")

    st.subheader("Income Entries")
    income_df = pd.DataFrame(st.session_state.income)
    if not income_df.empty:
        st.dataframe(income_df)
    else:
        st.info("No income data yet.")

with tab2:
    st.header("Log Expense")
    with st.form("expense_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            date = st.date_input("Date", value=datetime.today(), key="exp_date")
            amount = st.number_input("Amount (£)", min_value=0.0, step=5.0, key="exp_amount")
        with col2:
            expense_type = st.selectbox("Expense Type", ["Phone", "Mileage", "Software", "Repairs", "Utilities", "Other"])
            property_name = st.selectbox("Property", properties if properties else ["No properties found"], key="exp_prop")
        with col3:
            ownership = st.selectbox("Ownership Type", ownership_types, key="exp_owner")
            notes = st.text_input("Notes", key="exp_notes")
        submitted = st.form_submit_button("Add Expense")
        if submitted:
            entry = {
                "Date": date.strftime("%Y-%m-%d"),
                "Amount": amount,
                "Type": expense_type,
                "Property": property_name,
                "Ownership": ownership,
                "Notes": notes
            }
            add_entry(st.session_state.expenses, entry, "Expenses", property_name)
            st.success("Expense added.")

    st.subheader("Expense Entries")
    exp_df = pd.DataFrame(st.session_state.expenses)
    if not exp_df.empty:
        st.dataframe(exp_df)
    else:
        st.info("No expense data yet.")
