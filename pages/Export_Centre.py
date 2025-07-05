import streamlit as st
import pandas as pd
from datetime import datetime
from utils.drive_utils import upload_file_to_drive, create_drive_folder  # <-- Make sure this exists

st.title("📤 Export Centre")

# Column headers
income_cols = ["Date", "Amount", "Category", "Property", "Ownership"]
expense_cols = ["Date", "Amount", "Type", "Property", "Ownership"]
invoice_cols = ["Date", "Invoice Number", "Client", "Service", "Amount", "Property", "Ownership"]

# Load session data
income_df = pd.DataFrame(st.session_state.get("income", []), columns=income_cols)
expense_df = pd.DataFrame(st.session_state.get("expenses", []), columns=expense_cols)
invoice_df = pd.DataFrame(st.session_state.get("invoices", []), columns=invoice_cols)

# Parse dates
for df in [income_df, expense_df, invoice_df]:
    if not df.empty and "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])

# Filters
st.sidebar.header("📌 Export Filters")
years = list(range(2024, datetime.today().year + 2))
selected_year = st.sidebar.selectbox("Financial Year", [f"{y}-{y+1}" for y in years])
start_year = int(selected_year.split("-")[0])
start_date = datetime(start_year, 4, 1)
end_date = datetime(start_year + 1, 3, 31)

period = st.sidebar.selectbox("Period", ["Year", "6 Months", "Quarter", "Month"])
month_map = {1: "Jan", 2: "Feb", 3: "Mar", 4: "Apr", 5: "May", 6: "Jun",
             7: "Jul", 8: "Aug", 9: "Sep", 10: "Oct", 11: "Nov", 12: "Dec"}

properties = st.session_state.get("properties", [])
property_filter = st.sidebar.selectbox("Property", ["All"] + sorted(properties) if properties else ["All"])
ownership_filter = st.sidebar.selectbox("Ownership Type", ["All", "Personal", "Ltd"])

# Define export window
def get_export_range(period):
    if period == "Year":
        return start_date, end_date, "FY"
    elif period == "6 Months":
        mid = datetime(start_year, 10, 1)
        return (start_date, mid - pd.Timedelta(days=1), "H1")
    elif period == "Quarter":
        q_start = st.sidebar.selectbox("Start Month of Quarter", [4, 7, 10, 1])
        start = datetime(start_year if q_start != 1 else start_year + 1, q_start, 1)
        end = start + pd.DateOffset(months=3) - pd.Timedelta(days=1)
        label = f"Q{((q_start - 1)//3) + 1}"
        return start, end, label
    elif period == "Month":
        month = st.sidebar.selectbox("Month", list(range(1, 13)))
        start = datetime(start_year if month >= 4 else start_year + 1, month, 1)
        end = start + pd.DateOffset(months=1) - pd.Timedelta(days=1)
        label = f"{month_map[month]}"
        return start, end, label

range_start, range_end, range_label = get_export_range(period)

# Filter function
def filter_df(df):
    if df.empty or "Date" not in df.columns:
        return pd.DataFrame(columns=df.columns)
    df_filtered = df[(df["Date"] >= range_start) & (df["Date"] <= range_end)]
    if property_filter != "All":
        df_filtered = df_filtered[df_filtered["Property"] == property_filter]
    if ownership_filter != "All":
        df_filtered = df_filtered[df_filtered["Ownership"] == ownership_filter]
    return df_filtered

f_income = filter_df(income_df)
f_expense = filter_df(expense_df)
f_invoice = filter_df(invoice_df)

# P&L
st.subheader("📈 Profit & Loss Report")
total_income = f_income['Amount'].sum() if 'Amount' in f_income.columns else 0.0
total_expense = f_expense['Amount'].sum() if 'Amount' in f_expense.columns else 0.0
net_profit = total_income - total_expense
pl_df = pd.DataFrame([{
    "Total Income (£)": total_income,
    "Total Expenses (£)": total_expense,
    "Net Profit (£)": net_profit
}])
st.dataframe(pl_df)

# --- Drive Saving ---
folder_path = f"AccountingHQ/Exports/{property_filter}/{selected_year}/{range_label}"
create_drive_folder(folder_path)

# Export P&L
pl_csv = pl_df.to_csv(index=False)
st.download_button("Download P&L CSV", pl_csv, file_name="PnL_report.csv")
upload_file_to_drive(folder_path, pl_csv, "PnL_report.csv")

# Export Invoices
st.subheader("🧾 Invoice Summary")
if not f_invoice.empty:
    st.dataframe(f_invoice)
    inv_csv = f_invoice.to_csv(index=False)
    st.download_button("Download Invoices CSV", inv_csv, file_name="invoices_summary.csv")
    upload_file_to_drive(folder_path, inv_csv, "invoices_summary.csv")
else:
    st.info("No invoices found for selected filters.")

# Export Dividend Voucher
st.subheader("📜 Dividend Voucher Generator")
if not f_income.empty:
    div_amount = st.number_input("Dividend Amount (£)", min_value=0.0, step=50.0)
    shareholder = st.text_input("Shareholder Name", value="Your Name")
    if st.button("Generate Voucher") and div_amount > 0:
        voucher = (
            f"Dividend Voucher\n"
            f"Date: {datetime.now().date()}\n"
            f"Shareholder: {shareholder}\n"
            f"Property: {property_filter}\n"
            f"Amount: £{div_amount:.2f}\n"
            f"Ownership: {ownership_filter}"
        )
        st.text_area("Voucher Preview", value=voucher, height=150)
        st.download_button("Download Voucher", voucher.encode(), file_name="dividend_voucher.txt")
        upload_file_to_drive(folder_path, voucher.encode(), "dividend_voucher.txt")
else:
    st.info("Enter dividend details to generate a voucher.")
