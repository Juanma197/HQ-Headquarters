import streamlit as st
import pandas as pd
from datetime import datetime

st.title("📤 Export Centre")

income_cols = ["Date", "Amount", "Category", "Property", "Ownership"]
expense_cols = ["Date", "Amount", "Type", "Property", "Ownership"]
invoice_cols = ["Date", "Invoice Number", "Client", "Service", "Amount", "Property", "Ownership"]

income_df = pd.DataFrame(st.session_state.get("income", []), columns=income_cols)
expense_df = pd.DataFrame(st.session_state.get("expenses", []), columns=expense_cols)
invoice_df = pd.DataFrame(st.session_state.get("invoices", []), columns=invoice_cols)

for df in [income_df, expense_df, invoice_df]:
    if not df.empty and "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])

st.sidebar.header("📌 Export Filters")

years = list(range(2024, datetime.today().year + 2))
selected_year = st.sidebar.selectbox("Financial Year", [f"{y}-{y+1}" for y in years])
start_year = int(selected_year.split("-")[0])
start_date = datetime(start_year, 4, 1)
end_date = datetime(start_year + 1, 3, 31)

properties = st.session_state.get("properties", [])
property_filter = st.sidebar.selectbox("Property", ["All"] + sorted(properties) if properties else ["All"])
ownership_filter = st.sidebar.selectbox("Ownership Type", ["All", "Personal", "Ltd"])

def filter_df(df):
    if df.empty or "Date" not in df.columns:
        return pd.DataFrame(columns=df.columns)
    df_filtered = df[(df["Date"] >= start_date) & (df["Date"] <= end_date)]
    if property_filter != "All" and "Property" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["Property"] == property_filter]
    if ownership_filter != "All" and "Ownership" in df_filtered.columns:
        df_filtered = df_filtered[df_filtered["Ownership"] == ownership_filter]
    return df_filtered

f_income = filter_df(income_df)
f_expense = filter_df(expense_df)
f_invoice = filter_df(invoice_df)

st.subheader("📈 Profit & Loss Report")

total_income = f_income['Amount'].sum() if 'Amount' in f_income.columns else 0.0
total_expense = f_expense['Amount'].sum() if 'Amount' in f_expense.columns else 0.0
net_profit = total_income - total_expense

pl_data = {
    "Total Income (£)": total_income,
    "Total Expenses (£)": total_expense,
    "Net Profit (£)": net_profit
}
pl_df = pd.DataFrame([pl_data])
st.dataframe(pl_df)
st.download_button("Download P&L CSV", pl_df.to_csv(index=False), file_name="PnL_report.csv")

st.subheader("🧾 Invoice Summary")
if not f_invoice.empty:
    st.dataframe(f_invoice)
    st.download_button("Download Invoices CSV", f_invoice.to_csv(index=False), file_name="invoices_summary.csv")
else:
    st.info("No invoices found for selected filters.")

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
else:
    st.info("Enter dividend details to generate a voucher.")
