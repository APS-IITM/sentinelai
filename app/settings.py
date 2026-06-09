import streamlit as st

st.title("⚙️ Settings")

st.text_input("Splunk URL")
st.text_input("API Key", type="password")

st.button("Save Configuration")
st.toast("Saved locally")