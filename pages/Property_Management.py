import streamlit as st
import os
from datetime import datetime
from utils_drive import upload_to_drive, ensure_folder_path

st.title("🏠 Property Management")

if "properties" not in st.session_state:
    st.session_state["properties"] = []

# Add new property
with st.form("add_property_form"):
    new_prop = st.text_input("New Property Name / Address")
    if st.form_submit_button("Add Property") and new_prop:
        if new_prop not in st.session_state.properties:
            st.session_state.properties.append(new_prop)
            st.success(f"Added: {new_prop}")

# Property file uploads
if st.session_state.properties:
    st.subheader("📎 Upload Property Documents")
    selected_property = st.selectbox("Select Property", st.session_state.properties)
    file = st.file_uploader("Upload file for selected property")
    if file and st.button("📤 Upload to Drive"):
        today = datetime.today().strftime("%Y-%m")
        local_path = f"backups/{file.name}"
        with open(local_path, "wb") as f:
            f.write(file.read())
        upload_to_drive(f"AccountingHQ/{selected_property}/Backups/{today}/", local_path)
        st.success("File uploaded and saved.")

# Edit properties
if st.session_state.properties:
    st.subheader("✏️ Manage Properties")
    for idx, prop in enumerate(st.session_state.properties):
        col1, col2 = st.columns([4, 1])
        new_val = col1.text_input(f"Property {idx+1}", value=prop, key=f"edit_{idx}")
        if col2.button("Delete", key=f"del_{idx}"):
            st.session_state.properties.pop(idx)
            st.experimental_rerun()
        else:
            st.session_state.properties[idx] = new_val
else:
    st.info("Add a property to begin.")
