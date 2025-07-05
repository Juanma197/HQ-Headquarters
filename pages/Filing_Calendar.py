import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="📅 Filing Calendar", layout="centered")
st.title("📅 Filing Calendar & HMRC Reminders")

st.markdown("""
This calendar shows all the key deadlines for your Services Ltd:
- 🧾 VAT returns (quarterly)
- 🏢 Corporation Tax (CT600)
- 👤 Self Assessment
- 📜 Annual Accounts + Confirmation Statement
""")

today = datetime.today()
current_year = today.year

events = [
    {"Event": "VAT Return (Q1)", "Date": f"{current_year}-04-07"},
    {"Event": "VAT Return (Q2)", "Date": f"{current_year}-07-07"},
    {"Event": "VAT Return (Q3)", "Date": f"{current_year}-10-07"},
    {"Event": "VAT Return (Q4)", "Date": f"{current_year+1}-01-07"},
    {"Event": "CT600 (Corporation Tax)", "Date": f"{current_year+1}-06-30"},
    {"Event": "Self Assessment Deadline", "Date": f"{current_year+1}-01-31"},
    {"Event": "Annual Accounts Due", "Date": f"{current_year+1}-09-30"},
    {"Event": "Confirmation Statement", "Date": f"{current_year+1}-07-01"}
]

calendar_df = pd.DataFrame(events)
calendar_df["Date"] = pd.to_datetime(calendar_df["Date"])
calendar_df["Days Left"] = (calendar_df["Date"] - today).dt.days

st.subheader("🗓️ Upcoming Deadlines")
st.dataframe(calendar_df.sort_values(by="Date"), use_container_width=True)

st.subheader("⏰ Next 3 Deadlines")
st.table(calendar_df.sort_values(by="Date").head(3)[["Event", "Date", "Days Left"]])

st.markdown("---")
st.markdown("🔔 **Email Reminders Coming Soon** (Google Calendar integration planned)")
