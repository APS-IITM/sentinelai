"""
SentinelAI Operations Center
Splunk + MCP Observability Dashboard
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

st.title("⚙️ SentinelAI Operations Center")
st.caption(
    "Splunk • MCP • Detection • Intelligence Pipeline Visibility"
)

st.divider()

# ==========================================================
# SIDEBAR
# ==========================================================
st.sidebar.header("Dashboard Controls")

limit = st.sidebar.slider(
    "Results Per Query",
    min_value=5,
    max_value=100,
    value=20
)

show_raw = st.sidebar.checkbox(
    "Show Raw MCP Output",
    value=False
)

refresh = st.sidebar.button("🔄 Refresh Dashboard")

if refresh:
    st.rerun()

# ==========================================================
# TOOL INITIALIZATION
# ==========================================================
auth_tool = AuthTools()
network_tool = NetworkTools()
security_tool = SecurityTools()
system_tool = SystemTools()

# ==========================================================
# DATA COLLECTION
# ==========================================================
with st.spinner("Querying Splunk through MCP tools..."):

    start_time = time.time()

    try:
        auth_logs = auth_tool.get_auth_logs(limit=limit)
    except Exception as e:
        auth_logs = []
        st.error(f"AuthTools Error: {e}")

    try:
        network_logs = network_tool.get_network_logs(limit=limit)
    except Exception as e:
        network_logs = []
        st.error(f"NetworkTools Error: {e}")

    try:
        security_logs = security_tool.get_auth_logs(limit=limit)
    except Exception as e:
        security_logs = []
        st.error(f"SecurityTools Error: {e}")

    try:
        system_logs = system_tool.get_system_logs(limit=limit)
    except Exception as e:
        system_logs = []
        st.error(f"SystemTools Error: {e}")

    latency = round(time.time() - start_time, 2)

# ==========================================================
# METRICS
# ==========================================================
st.subheader("📊 Pipeline Health")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Auth Events", len(auth_logs))
c2.metric("Network Events", len(network_logs))
c3.metric("Security Events", len(security_logs))
c4.metric("System Events", len(system_logs))
c5.metric("Query Time", f"{latency}s")

st.divider()

# ==========================================================
# EVENT DISTRIBUTION
# ==========================================================
st.subheader("📈 MCP Tool Activity")

event_df = pd.DataFrame(
    {
        "Tool": [
            "Auth",
            "Network",
            "Security",
            "System"
        ],
        "Events": [
            len(auth_logs),
            len(network_logs),
            len(security_logs),
            len(system_logs)
        ]
    }
)

fig = px.bar(
    event_df,
    x="Tool",
    y="Events",
    title="Events Retrieved From Splunk"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ==========================================================
# COMPONENT HEALTH
# ==========================================================
st.subheader("🟢 Component Status")

health_df = pd.DataFrame(
    {
        "Component": [
            "AuthTools",
            "NetworkTools",
            "SecurityTools",
            "SystemTools"
        ],
        "Status": [
            "ONLINE" if auth_logs else "NO DATA",
            "ONLINE" if network_logs else "NO DATA",
            "ONLINE" if security_logs else "NO DATA",
            "ONLINE" if system_logs else "NO DATA"
        ]
    }
)

st.dataframe(
    health_df,
    use_container_width=True
)

st.divider()

# ==========================================================
# SPLUNK DATA TABS
# ==========================================================
tab1, tab2, tab3, tab4 = st.tabs(
    [
        "🔐 Authentication",
        "🌐 Network",
        "🛡 Security",
        "⚙️ System"
    ]
)

# ----------------------------------------------------------
# AUTH
# ----------------------------------------------------------
with tab1:

    st.subheader("Authentication Logs")

    if auth_logs:
        st.dataframe(
            pd.DataFrame(auth_logs),
            use_container_width=True
        )
    else:
        st.warning("No authentication logs returned.")

# ----------------------------------------------------------
# NETWORK
# ----------------------------------------------------------
with tab2:

    st.subheader("Network Logs")

    if network_logs:
        st.dataframe(
            pd.DataFrame(network_logs),
            use_container_width=True
        )
    else:
        st.warning("No network logs returned.")

# ----------------------------------------------------------
# SECURITY
# ----------------------------------------------------------
with tab3:

    st.subheader("Security Logs")

    if security_logs:
        st.dataframe(
            pd.DataFrame(security_logs),
            use_container_width=True
        )
    else:
        st.warning("No security logs returned.")

# ----------------------------------------------------------
# SYSTEM
# ----------------------------------------------------------
with tab4:

    st.subheader("System Logs")

    if system_logs:
        st.dataframe(
            pd.DataFrame(system_logs),
            use_container_width=True
        )
    else:
        st.warning("No system logs returned.")

# ==========================================================
# LOG VIEWER
# ==========================================================
st.divider()

st.subheader("📜 Runtime Logs")

LOG_FILE = "logs/sentinelai.log"

if os.path.exists(LOG_FILE):

    try:

        with open(
            LOG_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            logs = f.readlines()

        latest_logs = "".join(logs[-200:])

        st.code(
            latest_logs,
            language="text"
        )

    except Exception as e:

        st.error(
            f"Unable to load runtime logs: {e}"
        )

else:

    st.info(
        "Runtime log file not found."
    )

# ==========================================================
# DEBUG VIEW
# ==========================================================
if show_raw:

    st.divider()

    st.subheader("🔍 Raw MCP Output")

    st.json(
        {
            "auth_sample":
                auth_logs[:3] if auth_logs else [],

            "network_sample":
                network_logs[:3] if network_logs else [],

            "security_sample":
                security_logs[:3] if security_logs else [],

            "system_sample":
                system_logs[:3] if system_logs else []
        }
    )

# ==========================================================
# FOOTER
# ==========================================================
st.divider()

st.caption(
    f"SentinelAI Operations Center | "
    f"Last Updated: {time.strftime('%Y-%m-%d %H:%M:%S')}"
)