import streamlit as st
import pandas as pd
from datetime import datetime
from utils_drive import upload_to_drive

st.set_page_config(page_title="📅 Filing Calendar", layout="centered")
st.title("📅 Filing Calendar & HMRC Reminders")

properties = st.session_state.get("properties", [])
property_name = st.selectbox("Select Property", properties or ["No properties"])

events = [
    {"Event": "VAT Return (Q1)", "Date": f"{datetime.today().year}-04-07"},
    {"Event": "VAT Return (Q2)", "Date": f"{datetime.today().year}-07-07"},
    {"Event": "CT600 (Corp Tax)", "Date": f"{datetime.today().year + 1}-06-30"},
]

calendar_df = pd.DataFrame(events)
calendar_df["Date"] = pd.to_datetime(calendar_df["Date"])
calendar_df["Days Left"] = (calendar_df["Date"] - datetime.today()).dt.days

st.dataframe(calendar_df.sort_values("Date"), use_container_width=True)

st.subheader("🔔 Save Custom Reminder to Drive")
reminder_note = st.text_area("Write your filing reminder")
if st.button("📤 Save Reminder"):
    month = datetime.today().strftime("%Y-%m")
    local_file = f"backups/{property_name}_reminder_{month}.txt"
    with open(local_file, "w") as f:
        f.write(reminder_note)
    drive_path = f"AccountingHQ/{property_name}/Backups/{month}/"
    upload_to_drive(drive_path, local_file)
    st.success("Reminder saved and uploaded.")
