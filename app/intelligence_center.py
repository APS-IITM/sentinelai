import streamlit as st
from src.intelligence.engine import IntelligenceEngine

st.title("🧭 Cross-Domain Intelligence Center")
st.caption("Correlates isolated vector triggers into structural multi-stage attack story lines.")

if "active_threat_profiles" in st.session_state and st.session_state.active_threat_profiles:
    engine = IntelligenceEngine()
    
    with st.spinner("Processing framework cross-correlations..."):
        # Live processing via your custom intelligence module engine backend logic
        report = engine.analyze(st.session_state.active_threat_profiles)
        st.session_state.compiled_cti_report = report
        
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🔥 Correlated Campaign Context")
        st.metric("Inferred Campaign Profile", report.incident_type)
        st.metric("Peak Integrated Severity Context", report.severity)
        
        st.subheader("🎯 MITRE ATT&CK Mapping Profiles")
        for tech in report.mitre_techniques:
            st.markdown(f"`{tech}`")
            
    with col2:
        st.subheader("📖 Attack Progression Story Summary")
        st.info(report.attack_story)
        
        st.subheader("⏱️ Chronological Incident Audit Trail")
        for idx, event in enumerate(report.timeline, 1):
            st.markdown(f"**({idx})** `{event.get('time')}` | Asset Target Context: **{event.get('source')}** — Phase Classification Profile: `{event.get('attack')}` [`{event.get('severity')}`]")
else:
    st.warning("No threats available to run correlation engines against. Ensure data exists in Dashboard view.")