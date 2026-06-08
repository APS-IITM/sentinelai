import streamlit as st
import pandas as pd
import plotly.express as px
from src.anomaly.analyzer import AnomalyAnalyzer

st.title("✨ Executive System Overview")
st.caption("Active monitoring footprint leveraging mathematical signal anomaly extraction logic.")

# Execution of Anomaly Engine calculations for live counters
analyzer = AnomalyAnalyzer()
threat_profiles = []

if st.session_state.login_series:
    t = analyzer.analyze_series("Authentication Logs", st.session_state.login_series)
    if t: threat_profiles.append(t)
if st.session_state.error_series:
    t = analyzer.analyze_series("System Error Logs", st.session_state.error_series)
    if t: threat_profiles.append(t)
if st.session_state.network_series:
    t = analyzer.analyze_series("Network Perimeter Logs", st.session_state.network_series)
    if t: threat_profiles.append(t)

# Save computed threat profiles globally for down-stream view continuity
st.session_state.active_threat_profiles = threat_profiles

# Render KPI Metric Block
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Scanned Volume", f"{sum(st.session_state.login_series) + sum(st.session_state.error_series) + sum(st.session_state.network_series)} Logs")
col2.metric("Extracted Anomalies", f"{len(threat_profiles)} Triggered", delta_color="inverse")
col3.metric("Peak Core Risk Score", f"{max([t.score for t in threat_profiles]) if threat_profiles else 0.0:.1f} Score")
col4.metric("Infrastructure Node Links", "4 Connected (MCP)")

st.markdown("---")

# Chart Layout Split Core Elements
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("Time-Series Volumetric Trajectory")
    chart_data = pd.DataFrame({
        "Authentication Log Step": st.session_state.login_series,
        "System Error Step": st.session_state.error_series
    })
    fig = px.line(chart_data, color_discrete_sequence=["#D4AF37", "#C0C0C0"], template="plotly_white")
    fig.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=260)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Severity Weight Layout")
    sev_counts = [t.severity for t in threat_profiles] if threat_profiles else ["NORMAL"]
    df_pie = pd.DataFrame({"Severity": sev_counts}).value_counts().reset_index(name="Count")
    fig_pie = px.pie(df_pie, values="Count", names="Severity", 
                     color_discrete_sequence=["#8B0000", "#EAEAEA"], template="plotly_white")
    fig_pie.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=260, showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)