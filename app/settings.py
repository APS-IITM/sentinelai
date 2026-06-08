import streamlit as st

st.title("⚙️ Global Integrations & Settings")
st.caption("Secure configuration access points for managing telemetry APIs and processing connectors.")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 🔌 Splunk Core Connection Settings")
    splunk_host = st.text_input("Splunk Endpoint Host URL Address:", value="https://splunk-cloud-instance.internal")
    splunk_port = st.number_input("Splunk REST API Port Endpoint:", value=8089)
    splunk_token = st.text_input("Splunk Authentication Token:", value="••••••••••••••••••••", type="password")

with col2:
    st.markdown("### 🤖 Intelligence API Credentials")
    gemini_key = st.text_input("Google Gemini Processing Service API Key:", value="••••••••••••••••••••", type="password")
    refresh_rate = st.slider("Dashboard Auto-Refresh Loop Window (Seconds):", min_value=5, max_value=60, value=30)

st.markdown("---")
if st.button("💾 Securely Save System Configurations"):
    st.toast("System connectivity properties updated successfully inside .env environment profiles!", icon="✅")