import streamlit as st
from datetime import datetime
from drive_utils import connect_to_drive  # Make sure drive_utils.py exists

st.set_page_config(page_title="🏠 Welcome", layout="centered")

# Connect to Google Drive (only once)
drive = connect_to_drive()
st.success("✅ Google Drive connected successfully.")

# --- Language Selector ---
language = st.selectbox("🌐 Language / Idioma", ["English", "Español"])

# --- Content in both languages ---
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

    st.header("🚀 Quick Access")
    st.page_link("pages/Income_Tracker.py", label="📥 Income Tracker", icon="📥")
    #st.page_link("pages/Expense_Tracker.py", label="💸 Expense Tracker", icon="💸")
    st.page_link("pages/Invoice_Generator.py", label="📄 Invoice Generator", icon="📄")
    st.page_link("pages/Dashboard.py", label="📊 Dashboard", icon="📊")
    st.page_link("pages/Export_Centre.py", label="📤 Export Centre", icon="📤")
    st.page_link("pages/Salary_Dividend.py", label="👤 Salary & Dividends", icon="👤")
    st.page_link("pages/Filing_Calendar.py", label="📅 Filing Calendar", icon="📅")
    st.page_link("pages/Settings_Backup.py", label="⚙️ Settings & Backup", icon="⚙️")

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

    st.header("🚀 Acceso Rápido")
    st.page_link("pages/Income_Tracker.py", label="📥 Registro de Ingresos", icon="📥")
    #st.page_link("pages/Expense_Tracker.py", label="💸 Registro de Gastos", icon="💸")
    st.page_link("pages/Invoice_Generator.py", label="📄 Generador de Facturas", icon="📄")
    st.page_link("pages/Dashboard.py", label="📊 Panel de Control", icon="📊")
    st.page_link("pages/Export_Centre.py", label="📤 Centro de Exportación", icon="📤")
    st.page_link("pages/Salary_Dividend.py", label="👤 Sueldo y Dividendos", icon="👤")
    st.page_link("pages/Filing_Calendar.py", label="📅 Calendario Fiscal", icon="📅")
    st.page_link("pages/Settings_Backup.py", label="⚙️ Configuración y Copia de Seguridad", icon="⚙️")



