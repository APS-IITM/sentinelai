import streamlit as st

st.title("⚙️ Settings")
st.markdown("---")

st.text_input("Splunk Host", "https://localhost:8089")
st.text_input("API Key", type="password")

if st.button("Save"):
    st.success("Saved (session only)")