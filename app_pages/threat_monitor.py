import streamlit as st
import pandas as pd
from app_pages.ui_components.supabase_loader import get_anomalies
from src.ai.analyzer import AIAnalyzer

st.title("🔍 Tactical Threat Monitor")
st.caption("Live streaming event payloads ingested continuously through cloud storage instances")
st.markdown("---")

data = get_anomalies()

if not data:
    st.warning("Telemetry stream pipeline empty. No exceptions logged in this segment.")
    st.stop()

df = pd.DataFrame(data)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.markdown("#### Live Active Perimeters Events DataFrame")
st.dataframe(df, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

# Context Processing Section
st.markdown("### 🎯 Single-Event Triage Pipeline")
if 'id' in df.columns:
    selected_target = st.selectbox("Pick Threat Ref Record ID for targeted diagnosis", df['id'].tolist())
    
    if st.button("Generate On-Demand Forensic Audit"):
        target_series = df[df['id'] == selected_target].iloc[0]
        
        class EventDataWrapper:
            def __init__(self, item):
                self.source = str(item.get('source', 'NETWORK'))
                self.attack_type = str(item.get('attack_type', 'EXPLOIT'))
                self.severity = str(item.get('severity', 'LOW'))
                self.description = str(item.get('description', ''))
                self.data_points = int(item.get('data_points', 1))

        with st.spinner("Compiling contextual narrative logs..."):
            ai_engine = AIAnalyzer()
            analysis_output = ai_engine.analyze_event(EventDataWrapper(target_series))
            
            st.markdown(f"""
            <div class="card" style="border-left: 4px solid #D4AF37;">
                <h5>AI Forensic Intelligence Narrative: Block Ref #{selected_target}</h5>
                <p style="white-space: pre-wrap; color:#222; font-size:14px; line-height:1.6;">{analysis_output}</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.download_button(
                label="📥 Export Forensic Triage Log (.TXT)",
                data=analysis_output,
                file_name=f"Forensic_Audit_Ref_{selected_target}.txt",
                mime="text/plain"
            )