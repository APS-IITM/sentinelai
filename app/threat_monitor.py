import streamlit as st
import pandas as pd

st.title("🔍 Threat Monitor Feed")
st.caption("Live transactional stream from the Anomaly Detection Engine.")

# Filters bar
f1, f2, f3 = st.columns(3)
with f1:
    severity_filter = st.multiselect("Severity Status", ["Critical", "High", "Medium", "Low"], default=["Critical", "High"])
with f2:
    attack_type = st.selectbox("Attack Profile Filter", ["All Events", "Brute Force", "DDoS Spike", "Lateral Movement"])
with f3:
    search_query = st.text_input("Quick Filter Asset/IP", placeholder="e.g. 192.168.1.1")

# Master Threat Table
mock_feed = pd.DataFrame([
    {"Time": "16:21:05", "Source Entity": "10.0.4.152", "Attack Type": "Brute Force Attack", "Severity": "High", "Risk Score": 88},
    {"Time": "16:15:32", "Source Entity": "198.51.100.42", "Attack Type": "DDoS Stack Anomaly", "Severity": "Critical", "Risk Score": 96},
    {"Time": "15:44:12", "Source Entity": "Internal-HR-App", "Attack Type": "Network Scanning Active", "Severity": "Medium", "Risk Score": 64},
    {"Time": "14:22:01", "Source Entity": "User-Admin-Root", "Attack Type": "Privilege Escalation Spurt", "Severity": "Critical", "Risk Score": 92}
])

st.markdown("### Active Triage Queue")
st.dataframe(mock_feed, use_container_width=True, hide_index=True)

# Selected action item context linking
st.info("💡 Pro-Tip: Select an Incident ID from the sidebar or table to run a full Gemini Analysis inside the **AI Incident Reports** page.")