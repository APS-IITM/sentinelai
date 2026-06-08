import streamlit as st
from src.ai.analyzer import AIAnalyzer

st.title("🧠 Generative AI Forensic Report Hub")
st.caption("Routes structural incident payload properties directly to Google Gemini processing core parameters.")

if "active_threat_profiles" in st.session_state and st.session_state.active_threat_profiles:
    primary_threat = st.session_state.active_threat_profiles[0]
    
    # Inject context from correlated intelligence engine if available
    if "compiled_cti_report" in st.session_state and st.session_state.compiled_cti_report:
        cti = st.session_state.compiled_cti_report
        primary_threat.description = f"Multi-stage campaign correlated as {cti.incident_type}. Forensic trail: {cti.attack_story}"
        primary_threat.severity = cti.severity

    st.markdown("### 📄 Target Analysis Objective Selected:")
    st.info(f"Primary Target Node: **{primary_threat.source}** | Target Incident Profile Type: `{primary_threat.attack_type}`")

    if st.button("✨ Execute AI Deep Forensic Analysis"):
        try:
            ai_engine = AIAnalyzer()
            with st.spinner("Streaming context vectors to Google Gemini Core API layer..."):
                # Run the actual backend prompt compilation and model invocation
                ai_briefing = ai_engine.analyze_event(primary_threat)
                
            st.markdown("### 🧬 Automated Forensic Security Briefing")
            st.markdown(ai_briefing)
            st.success("Analysis report generated cleanly with no console logging interference.")
        except Exception as e:
            st.error(f"Failed to establish live connection to Gemini API Processing Layers: {e}")
else:
    st.warning("Please navigate back to the Dashboard to ingest data variables before requesting AI assistance templates.")