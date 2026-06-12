"""
SentinelAI Operations Center
Splunk + MCP Observability Dashboard (Animated SOC View)
"""

import os
import time
import pandas as pd
import plotly.express as px
import streamlit as st

from src.mcp_tools.auth_tools import AuthTools
from src.mcp_tools.network_tools import NetworkTools
from src.mcp_tools.security_tools import SecurityTools
from src.mcp_tools.system_tools import SystemTools


# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="SentinelAI Operations Center",
    page_icon="⚙️",
    layout="wide"
)

st.title("⚙️ SentinelAI SOC Operations Center")
st.caption("Real-Time Animated Splunk + MCP Intelligence Layer")

st.divider()


# ==========================================================
# SIDEBAR CONTROLS
# ==========================================================
st.sidebar.header("Controls")

limit = st.sidebar.slider("Results Per Query", 5, 100, 20)
auto_refresh = st.sidebar.checkbox("Enable Live Animation", value=True)
refresh_rate = st.sidebar.slider("Refresh Rate (sec)", 2, 15, 5)

manual_refresh = st.sidebar.button("🔄 Refresh Now")


# ==========================================================
# TOOL INIT
# ==========================================================
auth_tool = AuthTools()
network_tool = NetworkTools()
security_tool = SecurityTools()
system_tool = SystemTools()


# ==========================================================
# DATA COLLECTION
# ==========================================================
with st.spinner("Streaming Splunk telemetry via MCP..."):

    start_time = time.time()

    auth_logs = auth_tool.get_auth_logs(limit=limit)
    network_logs = network_tool.get_network_logs(limit=limit)
    security_logs = security_tool.get_auth_logs(limit=limit)
    system_logs = system_tool.get_system_logs(limit=limit)

    latency = round(time.time() - start_time, 2)


# ==========================================================
# METRICS PANEL
# ==========================================================
col1, col2, col3, col4, col5 = st.columns(5)

col1.metric("Auth Events", len(auth_logs))
col2.metric("Network Events", len(network_logs))
col3.metric("Security Events", len(security_logs))
col4.metric("System Events", len(system_logs))
col5.metric("Latency (s)", latency)

st.divider()


# ==========================================================
# EVENT STREAM DATAFRAME
# ==========================================================
event_df = pd.DataFrame({
    "Tool": ["Auth", "Network", "Security", "System"],
    "Events": [
        len(auth_logs),
        len(network_logs),
        len(security_logs),
        len(system_logs)
    ]
})


# ==========================================================
# 🎯 ANIMATED SOC LINE GRAPH
# ==========================================================
st.subheader("📈 Live MCP Event Stream (Animated)")

fig = px.line(
    event_df,
    x="Tool",
    y="Events",
    markers=True,
    line_shape="spline",
    color="Tool",   # DIFFERENT COLORS PER TOOL
    title="Real-Time Splunk → MCP Event Flow"
)

# 🔥 SOC VISUAL STYLING
fig.update_traces(
    line=dict(width=4),
    marker=dict(size=12),
    mode="lines+markers+text"
)

fig.update_layout(
    plot_bgcolor="#0b0f19",
    paper_bgcolor="#0b0f19",
    font=dict(color="white"),
    title_font=dict(size=20),
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.1)")
)

st.plotly_chart(fig, use_container_width=True)


# ==========================================================
# OPTIONAL SECOND ANIMATION (FLOW STYLE)
# ==========================================================
st.subheader("⚡ Attack Surface Activity Pulse")

pulse_df = pd.DataFrame({
    "time": list(range(len(event_df))),
    "intensity": event_df["Events"].values
})

pulse_fig = px.line(
    pulse_df,
    x="time",
    y="intensity",
    markers=True,
    line_shape="spline",
    color_discrete_sequence=["#00FFCC"],
    title="System Activity Pulse (Simulated SOC Wave)"
)

pulse_fig.update_traces(
    line=dict(width=3),
    marker=dict(size=8)
)

pulse_fig.update_layout(
    plot_bgcolor="#0b0f19",
    paper_bgcolor="#0b0f19",
    font=dict(color="white"),
    yaxis=dict(gridcolor="rgba(255,255,255,0.1)")
)

st.plotly_chart(pulse_fig, use_container_width=True)


# ==========================================================
# DATA TABLES (RAW VIEW)
# ==========================================================
st.divider()

tab1, tab2, tab3, tab4 = st.tabs(
    ["Auth", "Network", "Security", "System"]
)

with tab1:
    st.dataframe(pd.DataFrame(auth_logs), use_container_width=True)

with tab2:
    st.dataframe(pd.DataFrame(network_logs), use_container_width=True)

with tab3:
    st.dataframe(pd.DataFrame(security_logs), use_container_width=True)

with tab4:
    st.dataframe(pd.DataFrame(system_logs), use_container_width=True)


# ==========================================================
# AUTO REFRESH (ANIMATION EFFECT)
# ==========================================================
if auto_refresh:
    time.sleep(refresh_rate)
    st.rerun()

if manual_refresh:
    st.rerun()