import streamlit as st

st.title("⚙️ Engine Control Configuration")
st.caption("Global runtime environments and external connection setups")
st.markdown("---")

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("### SIEM Connection Interface")
splunk_url = st.text_input("Splunk Host URL Target", value="https://internal-siem.sentinel.local:8089")
api_key = st.text_input("Operational API Key Identifier", type="password", value="••••••••••••••••••••")

if st.button("Commit System Parameters"):
    st.toast("Configuration keys updated in session scope.", icon="⚙️")
st.markdown("</div>", unsafe_allow_html=True)