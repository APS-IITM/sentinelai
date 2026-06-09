import streamlit as st
import pandas as pd
from app_pages.ui.supabase_loader import get_ai_reports

st.title("🧠 AI Incident Reports")
st.caption("Autonomously built contextual breakdowns generated across analytical intervals")
st.markdown("---")

if st.button("Pull Compiled AI Reports"):
    with st.spinner("Extracting structural summaries..."):
        reports = get_ai_reports()
        
        if not reports:
            st.error("No generated strategic reports compiled in Database repository.")
            st.stop()
            
        for report in reports:
            st.markdown(f"""
            <div class="card">
                <h4 style="color:#D4AF37;">Report Reference ID: #{report.get('id', 'N/A')}</h4>
                <hr style="border:0; border-top:1px solid #EEEEEE; margin:10px 0;">
                <p style="font-size:15px; color:#222; line-height:1.6;">{report.get('generated_report', 'Missing report text block.')}</p>
            </div>
            """, unsafe_allow_html=True)