import streamlit as st
import pandas as pd

st.title("🏠 Property Management")

if "properties" not in st.session_state:
    st.session_state["properties"] = []

properties = st.session_state["properties"]

with st.form("add_property_form"):
    new_prop = st.text_input("New Property Name / Address")
    submitted = st.form_submit_button("Add Property")
    if submitted:
        if new_prop.strip() == "":
            st.warning("Please enter a valid property name.")
        elif new_prop in properties:
            st.warning("This property already exists.")
        else:
            properties.append(new_prop)
            st.success(f"Added property: {new_prop}")

if properties:
    st.subheader("Existing Properties")
    edited_properties = properties.copy()
    for idx, prop in enumerate(properties):
        cols = st.columns([4, 1, 1])
        edited_prop = cols[0].text_input(f"Property {idx + 1}", value=prop, key=f"prop_{idx}")
        edited_properties[idx] = edited_prop

        if cols[1].button("Save", key=f"save_{idx}"):
            if edited_prop.strip() == "":
                st.warning("Property name cannot be empty.")
            else:
                properties[idx] = edited_prop
                st.success(f"Property {idx + 1} updated.")

        if cols[2].button("Delete", key=f"del_{idx}"):
            properties.pop(idx)
            st.success(f"Property {idx + 1} deleted.")
            st.experimental_rerun()
else:
    st.info("No properties added yet.")
