import streamlit as st

st.title("⚙️ Global Cluster Integration Settings")
st.caption("Configure environment parameters, model criteria handles, and network access credentials.")

col1, col2 = st.columns(2)

with col1:
    st.subheader("🔌 Splunk Cloud Telemetry Ingress")
    splunk_url = st.text_input("Splunk REST Endpoint Address Host URL:", value="https://splunk-cloud-instance.internal:8089")
    splunk_user = st.text_input("Service Account Username Account Id:", value="sentinel_service_orchestrator")
    splunk_pass = st.text_input("Service Account Password / API Token Key Set:", value="••••••••••••••••••••", type="password")

with col2:
    st.subheader("🤖 Generative LLM Orchestration Control")
    st.selectbox("Target Core Model Endpoint Parameter Matrix:", ["Google Gemini Pro (Default Production)", "Google Gemini Flash (Ultra Low Latency Node)"])
    gemini_key = st.text_input("Google AI Developer Studio Endpoint Core Access Key:", value="••••••••••••••••••••", type="password")

st.markdown("---")
if st.button("💾 Apply Configuration Parameters"):
    st.toast("System connectivity variables committed safely to local execution pipelines!", icon="✅")