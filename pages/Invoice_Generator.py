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




st.title("📄 Invoice Generator")

if 'invoices' not in st.session_state:
    st.session_state.invoices = []
if 'properties' not in st.session_state:
    st.session_state.properties = []

properties = st.session_state["properties"]
ownership_types = ["Personal", "Ltd"]
services = {
    "Management Fee": 120.0,
    "Consulting": 80.0,
    "Admin Support": 60.0
}

drive = connect_to_drive()

st.header("Create New Invoice")
with st.form("invoice_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        date = st.date_input("Invoice Date", value=datetime.today())
        invoice_number = st.text_input("Invoice Number", value=f"INV-{len(st.session_state.invoices)+1:03}")
    with col2:
        service = st.selectbox("Service Type", list(services.keys()))
        amount = services[service]
    with col3:
        property_name = st.selectbox("Property", properties if properties else ["No properties found"])
        ownership = st.selectbox("Ownership Type", ownership_types)
        client_name = st.text_input("Client Name", value="Property Holding Ltd")

    notes = st.text_area("Notes (optional)", value=f"Monthly charge for {service} at {property_name}")
    submitted = st.form_submit_button("Generate Invoice")

    if submitted:
        invoice_data = {
            "Invoice Number": invoice_number,
            "Date": date.strftime("%Y-%m-%d"),
            "Client": client_name,
            "Service": service,
            "Amount": amount,
            "Property": property_name,
            "Ownership": ownership,
            "Notes": notes
        }
        st.session_state.invoices.append(invoice_data)
        st.success(f"Invoice {invoice_number} generated.")

        # Save to Drive
        folder_ids = ensure_property_structure(drive, property_name)
        save_path = tempfile.NamedTemporaryFile(delete=False, suffix=".json").name
        with open(save_path, "w") as f:
            json.dump(invoice_data, f, indent=2)
        upload_file_to_drive(drive, folder_ids["Invoices"], save_path)

st.subheader("🧾 Invoice Log")
invoice_df = pd.DataFrame(st.session_state.invoices)
if not invoice_df.empty:
    st.dataframe(invoice_df)

    st.subheader("📎 Preview an Invoice")
    selected = st.selectbox("Select Invoice to Preview", invoice_df["Invoice Number"].tolist())
    selected_inv = invoice_df[invoice_df["Invoice Number"] == selected].iloc[0]

    with st.expander("📄 Invoice Preview"):
        st.markdown(f"""
        **Invoice Number**: {selected_inv['Invoice Number']}  
        **Date**: {selected_inv['Date']}  
        **Client**: {selected_inv['Client']}  
        **Service**: {selected_inv['Service']}  
        **Property**: {selected_inv['Property']}  
        **Amount**: £{selected_inv['Amount']:.2f}  
        **Ownership**: {selected_inv['Ownership']}  
        **Notes**: {selected_inv['Notes']}
        """)
else:
    st.info("No invoices created yet.")
