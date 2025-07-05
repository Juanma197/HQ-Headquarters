import streamlit as st
import pandas as pd
from datetime import datetime

st.title("📥 Income & 💸 Expense Tracker")

if 'income' not in st.session_state:
    st.session_state.income = []
if 'expenses' not in st.session_state:
    st.session_state.expenses = []
if 'properties' not in st.session_state:
    st.session_state.properties = []

ownership_types = ["Personal", "Ltd"]
properties = st.session_state["properties"]

def add_entry(storage, entry):
    storage.append(entry)

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
            add_entry(st.session_state.income, {
                "Date": date,
                "Amount": amount,
                "Category": category,
                "Property": property_name,
                "Ownership": ownership,
                "Notes": notes
            })
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
            add_entry(st.session_state.expenses, {
                "Date": date,
                "Amount": amount,
                "Type": expense_type,
                "Property": property_name,
                "Ownership": ownership,
                "Notes": notes
            })
            st.success("Expense added.")

    st.subheader("Expense Entries")
    exp_df = pd.DataFrame(st.session_state.expenses)
    if not exp_df.empty:
        st.dataframe(exp_df)
    else:
        st.info("No expense data yet.")
