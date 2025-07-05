import streamlit as st
import pandas as pd
from datetime import datetime
import plotly.express as px

st.title("📊 Monthly Accounting Dashboard")

# Columns expected in session_state
income_cols = ["Date", "Amount", "Category", "Property", "Ownership"]
expense_cols = ["Date", "Amount", "Type", "Property", "Ownership"]
invoice_cols = ["Date", "Invoice Number", "Client", "Service", "Amount", "Property", "Ownership"]

# Load data from session state
income_df = pd.DataFrame(st.session_state.get("income", []), columns=income_cols)
expense_df = pd.DataFrame(st.session_state.get("expenses", []), columns=expense_cols)
invoice_df = pd.DataFrame(st.session_state.get("invoices", []), columns=invoice_cols)

# Parse dates if present
for df in [income_df, expense_df, invoice_df]:
    if not df.empty and "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])

# Sidebar filter: Financial year selection (April 1 to March 31)
st.sidebar.header("📌 Filters")
years = list(range(2024, datetime.today().year + 2))
selected_year = st.sidebar.selectbox("Financial Year", [f"{y}-{y+1}" for y in years])

# Extract start and end dates for financial year
start_year = int(selected_year.split("-")[0])
start_date = datetime(start_year, 4, 1)
end_date = datetime(start_year + 1, 3, 31)

# Property filter
properties = st.session_state.get("properties", [])
property_filter = st.sidebar.selectbox("Property", ["All"] + sorted(properties) if properties else ["All"])

# Ownership filter
ownership_filter = st.sidebar.selectbox("Ownership Type", ["All", "Personal", "Ltd"])

# Filter function for financial year and other filters
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

# Metrics
col1, col2, col3 = st.columns(3)
if not f_income.empty:
    col1.metric("💰 Total Income", f"£{f_income['Amount'].sum():,.2f}")
else:
    col1.info("No income data.")

if not f_expense.empty:
    col2.metric("💸 Total Expenses", f"£{f_expense['Amount'].sum():,.2f}")
else:
    col2.info("No expense data.")

if not f_income.empty and not f_expense.empty:
    net_profit = f_income['Amount'].sum() - f_expense['Amount'].sum()
    col3.metric("📈 Net Profit", f"£{net_profit:,.2f}")
else:
    col3.info("Net profit not available.")

# Charts
st.subheader("📊 Breakdown Charts")

if not f_income.empty:
    inc_chart = px.bar(
        f_income.groupby("Category")["Amount"].sum().reset_index(),
        x="Category", y="Amount", title="Income by Category", color="Category"
    )
    st.plotly_chart(inc_chart, use_container_width=True)
else:
    st.info("No income data available for selected period.")

if not f_expense.empty:
    exp_chart = px.pie(
        f_expense, values="Amount", names="Type", title="Expense Breakdown by Type"
    )
    st.plotly_chart(exp_chart, use_container_width=True)
else:
    st.info("No expense data available for selected period.")

# Top 5 expenses
st.subheader("🔍 Top 5 Expenses")
if not f_expense.empty:
    top_exp = f_expense.sort_values(by="Amount", ascending=False).head(5)
    st.table(top_exp[["Date", "Type", "Amount", "Property"]])
else:
    st.info("No expenses recorded for this period.")
