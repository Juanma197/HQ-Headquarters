import streamlit as st
import json
from datetime import date, datetime
from dateutil.parser import parse

st.set_page_config(page_title="⚙️ Settings & Backup", layout="centered")
st.title("⚙️ Settings & Data Backup")

# --- Session Setup ---
if 'income' not in st.session_state:
    st.session_state.income = []
if 'expenses' not in st.session_state:
    st.session_state.expenses = []
if 'invoices' not in st.session_state:
    st.session_state.invoices = []
if 'properties' not in st.session_state:
    st.session_state.properties = []

# --- Save Function ---
def save_data():
    def convert_dates(entries):
        new_entries = []
        for entry in entries:
            new_entry = {}
            for k, v in entry.items():
                if isinstance(v, (date, datetime)):
                    new_entry[k] = v.isoformat()
                else:
                    new_entry[k] = v
            new_entries.append(new_entry)
        return new_entries

    data = {
        "income": convert_dates(st.session_state.income),
        "expenses": convert_dates(st.session_state.expenses),
        "invoices": convert_dates(st.session_state.invoices),
        "properties": st.session_state.properties
    }
    with open("accounting_backup.json", "w") as f:
        json.dump(data, f, indent=2)
    return "accounting_backup.json"

# --- Load Function ---
def load_data():
    try:
        with open("accounting_backup.json", "r") as f:
            data = json.load(f)
            def parse_dates(entries):
                for entry in entries:
                    for k, v in entry.items():
                        if isinstance(v, str):
                            try:
                                parsed_date = parse(v)
                                if parsed_date.time() == datetime.min.time():
                                    entry[k] = parsed_date.date()
                                else:
                                    entry[k] = parsed_date
                            except:
                                pass
                return entries

            st.session_state.income = parse_dates(data.get("income", []))
            st.session_state.expenses = parse_dates(data.get("expenses", []))
            st.session_state.invoices = parse_dates(data.get("invoices", []))
            st.session_state.properties = data.get("properties", [])
            return True
    except Exception as e:
        st.error(f"Failed to load backup: {e}")
        return False

# --- UI ---
st.subheader("💾 Save Your Data")
if st.button("📤 Save Now"):
    file_path = save_data()
    st.success(f"Data saved to {file_path}")

st.subheader("📥 Load Previous Backup")
if st.button("📥 Load Backup"):
    if load_data():
        st.success("Backup loaded successfully!")
    else:
        st.error("Failed to load backup. Make sure 'accounting_backup.json' exists.")

st.subheader("🔄 Reset Data (Danger Zone)")
if st.button("❌ Clear All Data"):
    st.session_state.income = []
    st.session_state.expenses = []
    st.session_state.invoices = []
    st.session_state.properties = []
    st.success("All session data cleared!")
