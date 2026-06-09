import streamlit as st
import pandas as pd
from app_pages.ui_components.supabase_loader import get_intel_reports, get_anomalies

st.title("🧭 Intelligence Center")
st.caption("Correlate active threat profiles using pre-evaluated data streams")
st.markdown("---")

if st.button("Query Real-time Intelligence Framework"):
    with st.spinner("Accessing threat layers..."):
        reports = get_intel_reports()
        
        if not reports:
            st.info("No validated structural threat intelligence documents found in database records.")
            st.stop()
            
        for report in reports:
            with st.container():
                st.markdown(f"""
                <div class="card">
                    <h3 style="margin-top:0; color:#111;">Type: {report.get('incident_type', 'Unclassified')}</h3>
                    <p style="color:#666;"><b>Severity Vector:</b> {report.get('severity', 'UNKNOWN')}</p>
                    <div style="background:#FDFDFD; padding:12px; border-left:3px solid #D4AF37; border-radius:4px;">
                        {report.get('attack_story', 'No story parameters written.')}
                    </div>
                </div>
                """, unsafe_allow_html=True)