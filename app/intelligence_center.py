import streamlit as st
from src.intelligence.engine import IntelligenceEngine

st.title("🧭 Intelligence Center")

if st.button("Run CTI Correlation (from stored data)"):

    if not st.session_state.active_threat_profiles:
        st.warning("No threat data available")
        st.stop()

    engine = IntelligenceEngine()
    report = engine.analyze(st.session_state.active_threat_profiles)

    st.session_state.compiled_cti_report = report

    st.success("CTI Report Generated")

    st.write("Incident:", report.incident_type)
    st.write("Severity:", report.severity)
    st.write(report.attack_story)