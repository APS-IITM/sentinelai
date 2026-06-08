import streamlit as st
import pandas as pd

st.title("🔍 Active Threat Monitor Feed")
st.caption("Real-time telemetry stream parsing extracted mathematical anomalies.")

if "active_threat_profiles" in st.session_state and st.session_state.active_threat_profiles:
    # Convert Pydantic ThreatEvent object values to clean frontend table rows
    threat_table_data = []
    for t in st.session_state.active_threat_profiles:
        threat_table_data.append({
            "Target Log Source": t.source,
            "Engine Tag": t.anomaly_type,
            "Assigned Severity": t.severity,
            "Risk Score Index": f"{t.score:.2f}",
            "Inferred Attack Type": t.attack_type,
            "Latest Volumetric Data Point": t.data_points
        })
    
    st.dataframe(pd.DataFrame(threat_table_data), use_container_width=True, hide_index=True)
else:
    st.info("🟢 Clean Slate: Core pipeline engines reporting zero mathematical vector indicators.")