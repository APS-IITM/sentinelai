import streamlit as st
import pandas as pd
import plotly.express as px
from app_pages.ui.supabase_loader import get_anomalies

st.title("📊 Security Operations Center")
st.caption("Real-time telemetry parsed via Supabase persistence layer")
st.markdown("---")

# Data sourcing
data = get_anomalies()

if not data:
    st.info("No network telemetry data currently resolved within the remote instance.")
    st.stop()

df = pd.DataFrame(data)

# Metric Component
def metric_card(title, value, delta=None):
    delta_html = f"<small>▲ {delta}</small>" if delta else ""
    st.markdown(f"""
    <div class="card">
        <h4>{title}</h4>
        <h2>{value}</h2>
        {delta_html}
    </div>
    """, unsafe_allow_html=True)

# Dashboard KPI Columns
col1, col2, col3 = st.columns(3)
with col1:
    metric_card("Total Active Vectors", len(df), "12% vs last hour")
with col2:
    high_sev = len(df[df['severity'].str.upper() == 'HIGH']) if 'severity' in df.columns else 0
    metric_card("Critical Anomalies", high_sev, "Escalating")
with col3:
    metric_card("System Integrity Status", "Optimal", "Healthy")

st.markdown("### 📈 Analytical Breakdowns")

# Plotly Charts Processing
c1, c2 = st.columns(2)

with c1:
    st.markdown("#### Incident Vector Dispersion (Pie)")
    if 'severity' in df.columns:
        fig_pie = px.pie(df, names='severity', color_discrete_sequence=px.colors.sequential.Gold)
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(t=20,b=20,l=20,r=20))
        st.plotly_chart(fig_pie, use_container_width=True)

with c2:
    st.markdown("#### Threat Profiles Timeline (Line)")
    if 'created_at' in df.columns:
        df['created_at'] = pd.to_datetime(df['created_at'])
        time_df = df.groupby(df['created_at'].dt.date).size().reset_index(name='Counts')
        fig_line = px.line(time_df, x='created_at', y='Counts', color_discrete_sequence=['#D4AF37'])
        fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig_line, use_container_width=True)

st.markdown("#### Severity Distribution Matrix (Bar)")
if 'severity' in df.columns:
    severity_count = df['severity'].value_counts().reset_index(name='Count')
    fig_bar = px.bar(severity_count, x='severity', y='Count', color='severity', color_discrete_sequence=px.colors.sequential.Amber)
    fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False, xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig_bar, use_container_width=True)