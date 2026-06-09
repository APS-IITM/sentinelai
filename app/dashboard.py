import streamlit as st
import pandas as pd
from src.storage.anomaly_store import AnomalyStore

st.title("📊 Dashboard Overview")
st.caption("Passive data-driven SOC analytics")

data = AnomalyStore.get_all()

st.session_state.active_threat_profiles = data

if not data:
    st.info("No anomaly data available in storage.")
    st.stop()

# Metrics
st.metric("Total Incidents", len(data))

severity_count = {}
for d in data:
    severity_count[d.get("severity", "LOW")] = severity_count.get(d.get("severity", "LOW"), 0) + 1

st.bar_chart(severity_count)

# Table view
st.dataframe(pd.DataFrame(data))