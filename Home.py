import streamlit as st
from drive_utils import connect_to_drive, ensure_property_structure
from datetime import datetime

st.set_page_config(page_title="🏠 Welcome", layout="centered")
st.title("📁 Google Drive Test")

# Connect to Drive
drive = connect_to_drive()
st.success("✅ Google Drive connected successfully.")

# Property selection
property_name = st.selectbox("Select Property", ["Example House 1", "Example House 2", "Add New..."], index=0)
if property_name == "Add New...":
    property_name = st.text_input("Enter New Property Name")
    if not property_name:
        st.stop()

# Ensure folder structure
folder_ids = ensure_property_structure(drive, property_name)

# Display folders
st.subheader(f"📂 Folders for {property_name}")
for category, fid in folder_ids.items():
    st.markdown(f"- **{category}** → Folder ID: `{fid}`")

# Optional: Display full usage in English/Spanish
language = st.selectbox("🌐 Language / Idioma", ["English", "Español"])

if language == "English":
    st.title("🏠 Welcome to Your Accounting HQ")
    st.markdown("""
    This app helps you run all financial tasks for your Services Ltd:

    - Track **income and expenses**
    - Generate and download **invoices**
    - View charts in the **Dashboard**
    - Export **HMRC-ready reports**
    - Simulate **salary and dividends**
    - Get notified about tax **deadlines**
    - Backup your data easily
    """)

elif language == "Español":
    st.title("🏠 Bienvenido a tu Sede Contable")
    st.markdown("""
    Esta aplicación te ayuda a gestionar todas las tareas financieras de tu empresa Services Ltd:

    - Registrar **ingresos y gastos**
    - Crear y descargar **facturas**
    - Ver gráficos en el **Panel de Control**
    - Exportar **informes para HMRC**
    - Simular **sueldo y dividendos**
    - Ver plazos de **presentaciones fiscales**
    - Hacer copias de seguridad fácilmente
    """)
