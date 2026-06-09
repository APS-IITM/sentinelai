import streamlit as st
import pandas as pd
from app_pages.ui.supabase_loader import get_ai_reports
from src.ai.analyzer import AIAnalyzer

st.title("🧠 AI Analytics Reports Command")
st.caption("Review autonomous threat matrices or run localized text-document exports.")
st.markdown("---")

stored_briefs = get_ai_reports()

if not stored_briefs:
    st.info("No compiled technical documentation assets available inside Database inventory.")
else:
    options_map = {f"Executive Summary Briefing #{doc.get('id')} - Scope Target: {str(doc.get('source_type')).upper()}": doc for doc in stored_briefs}
    selection = st.selectbox("Select Target Analytics Package to Load", list(options_map.keys()))
    
    if selection:
        selected_record = options_map[selection]
        
        st.markdown(f"""
        <div class="card">
            <h3 style="margin-top:0; color:#111;">{selection}</h3>
            <p style="color:#666;"><b>Highest Logged Severity Factor:</b> <span style="color:#D4AF37; font-weight:600;">{selected_record.get('highest_severity')}</span></p>
            <p style="color:#666;"><b>Sampled Dataset Events Count:</b> {selected_record.get('event_count', 'N/A')}</p>
            <hr style="border:0; border-top:1px solid #EAEAEA; margin:16px 0;">
            <div style="background:#FAFBAF; padding:20px; border-radius:8px; line-height:1.6; color:#111; font-size:14px; white-space:pre-wrap;">{selected_record.get('generated_report')}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.download_button(
            label="📥 Export Intelligence Document (.TXT)",
            data=str(selected_record.get('generated_report', '')),
            file_name=f"SentinelAI_ExecutiveBriefing_{selected_record.get('id')}.txt",
            mime="text/plain"
        )