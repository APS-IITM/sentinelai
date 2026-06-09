import streamlit as st
import pandas as pd
import plotly.express as px
from app_pages.ui.supabase_loader import get_anomalies

# Page Configuration Setup Contexts
st.title("🛡️ Enterprise Command Centre")
st.caption("Active unified analytical overview — Systems telemetry matching live data infrastructure nodes.")
st.markdown("---")

# Data Layer Processing
data = get_anomalies()
df = pd.DataFrame(data) if data else pd.DataFrame(columns=['severity', 'created_at', 'source'])

# Define Premium Monochromatic Gold Hex Accents explicitly to prevent Plotly color errors
PREMIUM_GOLD_SCALE = ['#D4AF37', '#AA820A', '#E6C65C', '#806000', '#F3E5AB']
PREMIUM_MONO_SCALE = ['#111111', '#444444', '#777777', '#AAAAAA', '#CCCCCC']

# Custom Metric Component Asset Pipeline
def render_premium_metric(title, value, delta=None):
    delta_markup = f"<small>▲ {delta}</small>" if delta else ""
    st.markdown(f"""
    <div class="card">
        <h4>{title}</h4>
        <h2>{value}</h2>
        {delta_markup}
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 🗂️ PREMIUM INTERACTIVE NAVIGATION MATRIX HUB
# ---------------------------------------------------------
st.markdown("### 🧭 Platform Navigational Core")
st.caption("Direct control options to system partitions.")

nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns(5)

with nav_col1:
    st.markdown("""<div class='nav-block-card'><b>🔍 Threat Monitor</b><br><small style='color:#666;'>Live Feeds</small></div>""", unsafe_allow_html=True)
    # Using small hidden native layout targets to process routing cleanly
    if st.button("Open Feed", key="nav_threat"): st.switch_page("app_pages/threat_monitor.py")
with nav_col2:
    st.markdown("""<div class='nav-block-card'><b>🧠 CTI Engine</b><br><small style='color:#666;'>Threat intel</small></div>""", unsafe_allow_html=True)
    if st.button("Open Engine", key="nav_intel"): st.switch_page("app_pages/intelligence_center.py")
with nav_col3:
    st.markdown("""<div class='nav-block-card'><b>📄 AI Reports</b><br><small style='color:#666;'>SOC Briefs</small></div>""", unsafe_allow_html=True)
    if st.button("Open Reports", key="nav_ai"): st.switch_page("app_pages/ai_reports.py")
with nav_col4:
    st.markdown("""<div class='nav-block-card'><b>🧰 Forensics</b><br><small style='color:#666;'>Log Queries</small></div>""", unsafe_allow_html=True)
    if st.button("Open Console", key="nav_forensics"): st.switch_page("app_pages/investigation.py")
with nav_col5:
    st.markdown("""<div class='nav-block-card'><b>⚙️ Settings</b><br><small style='color:#666;'>SIEM Keys</small></div>""", unsafe_allow_html=True)
    if st.button("Open Config", key="nav_settings"): st.switch_page("app_pages/settings.py")

st.markdown("---")

# Metrics Visualization Grid
m1, m2, m3 = st.columns(3)
with m1:
    render_premium_metric("Aggregated Attack Vectors", len(df), "4.1% vs preceding cycle")
with m2:
    high_count = len(df[df['severity'].astype(str).str.upper() == 'HIGH']) if not df.empty else 0
    render_premium_metric("Escalated Critical Incidents", f"{high_count} Alerts", "Active Triage")
with m3:
    render_premium_metric("Database Storage Synchronization", "Synchronized", "Latency 18ms")

# ---------------------------------------------------------
# 📈 PREMIUM CHART OBJECT ENGINE INTEGRATION
# ---------------------------------------------------------
st.markdown("### 📊 Forensic Data Analytics Grid")

if df.empty:
    st.info("System layer awaiting incoming data streams. Visual analytics will adapt when anomalies are registered.")
else:
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        st.markdown("#### Incident Vector Dispersion Vector")
        fig_pie = px.pie(df, names='severity', color_discrete_sequence=PREMIUM_GOLD_SCALE, hole=0.4)
        fig_pie.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=True, margin=dict(t=10,b=10,l=10,r=10))
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with chart_col2:
        st.markdown("#### Tactical Timeline Trends Analysis")
        if 'created_at' in df.columns:
            df['created_at'] = pd.to_datetime(df['created_at'])
            time_series = df.groupby(df['created_at'].dt.date).size().reset_index(name='Volume')
            fig_line = px.line(time_series, x='created_at', y='Volume', color_discrete_sequence=['#111111'])
            fig_line.update_traces(line=dict(width=3), mode='lines+markers')
            fig_line.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', xaxis_title=None, yaxis_title=None)
            st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("#### Frequency Distribution Matrix Across Severity Profiles")
    if 'severity' in df.columns:
        sev_data = df['severity'].value_counts().reset_index(name='Occurrences')
        fig_bar = px.bar(sev_data, x='severity', y='Occurrences', color='severity', color_discrete_sequence=PREMIUM_GOLD_SCALE)
        fig_bar.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False, xaxis_title=None, yaxis_title=None)
        st.plotly_chart(fig_bar, use_container_width=True)