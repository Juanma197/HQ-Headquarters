import streamlit as st
import json
from datetime import datetime
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




st.set_page_config(page_title="Salary & Dividend Simulator", layout="centered")
st.title("👤 Salary + Dividend Simulator")

# Constants
CORP_TAX_RATE = 0.19
DIVIDEND_ALLOWANCE = 500
BASIC_RATE = 0.075
HIGHER_RATE = 0.3375
SALARY_PERSONAL_ALLOWANCE = 12570

# Session properties
if "properties" not in st.session_state:
    st.session_state["properties"] = []

st.markdown("""
This tool helps you simulate how to pay yourself through **salary** and **dividends**.
It calculates:
- How much Corporation Tax you pay
- Your personal tax from dividends and salary
- Estimated take-home pay
""")

# Inputs
profit = st.number_input("Enter total profit (£)", min_value=0.0, step=100.0)
salary = st.slider("Annual Salary (£)", 0, 50000, 12570, step=100)
dividends = st.slider("Dividends (£)", 0, 100000, 10000, step=500)

# Calculations
taxable_profit = max(0, profit - salary)
corp_tax = taxable_profit * CORP_TAX_RATE

salary_taxable = max(0, salary - SALARY_PERSONAL_ALLOWANCE)
salary_tax = salary_taxable * 0.2 if salary_taxable > 0 else 0

dividend_taxable = max(0, dividends - DIVIDEND_ALLOWANCE)
dividend_tax = 0
if dividend_taxable <= 50270 - salary:
    dividend_tax = dividend_taxable * BASIC_RATE
else:
    basic_portion = max(0, 50270 - salary - DIVIDEND_ALLOWANCE)
    higher_portion = dividend_taxable - basic_portion
    dividend_tax = basic_portion * BASIC_RATE + higher_portion * HIGHER_RATE

total_personal_tax = salary_tax + dividend_tax
total_corp_tax = corp_tax
total_tax = total_personal_tax + total_corp_tax
take_home = salary + dividends - total_personal_tax

# Display Results
col1, col2 = st.columns(2)
with col1:
    st.metric("👤 Total Personal Tax", f"£{total_personal_tax:,.2f}")
    st.metric("🏢 Corporation Tax", f"£{total_corp_tax:,.2f}")
with col2:
    st.metric("💷 Take-Home Pay", f"£{take_home:,.2f}")
    st.metric("📉 Total Tax Paid", f"£{total_tax:,.2f}")

# Tip
st.subheader("💡 Tip")
if salary <= SALARY_PERSONAL_ALLOWANCE:
    st.success("You're optimising salary below the tax-free allowance.")
elif salary <= 12570 + 1000:
    st.info("You're slightly above the allowance — some tax will apply.")
else:
    st.warning("You may want to reduce salary to stay within the £12,570 personal allowance.")

# 💾 Save to Google Drive
st.markdown("---")
st.subheader("💾 Save This Simulation")

properties = st.session_state["properties"]
if properties:
    selected_property = st.selectbox("Choose Property to Save Under", properties)
    if st.button("📤 Save to Drive"):
        drive = connect_to_drive()
        folder_ids = ensure_property_structure(drive, selected_property)
        backup_folder = folder_ids["Backups"]

        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"salary_sim_{timestamp}.json"
        tmp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".json").name

        save_data = {
            "Date": timestamp,
            "Profit": profit,
            "Salary": salary,
            "Dividends": dividends,
            "Corporation Tax": total_corp_tax,
            "Personal Tax": total_personal_tax,
            "Total Tax": total_tax,
            "Take-Home": take_home
        }

        with open(tmp_path, "w") as f:
            json.dump(save_data, f, indent=2)

        upload_file_to_drive(drive, backup_folder, tmp_path)
        st.success("Simulation saved to Drive.")
else:
    st.info("Please add at least one property in the Property Management page to save simulations.")

