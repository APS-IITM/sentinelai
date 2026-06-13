"""
SentinelAI Splunk Dashboard
LIVE MODE: Real-time MCP + Daemon Feed + Alerts + Bounded RAM Log Stream
"""

import sys
import time
import socket
import threading
import pandas as pd
import streamlit as st

from src.mcp_tools.auth_tools import AuthTools
from src.mcp_tools.network_tools import NetworkTools
from src.mcp_tools.security_tools import SecurityTools
from src.mcp_tools.system_tools import SystemTools

from src.alerts.global_alerts import GlobalAlertStore


# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="SentinelAI Splunk Live Dashboard",
    layout="wide"
)

st.title("⚙️ SentinelAI Splunk Live Stream")
st.caption("Real-time MCP → Splunk → Daemon → Alert Pipeline")

st.divider()


# ==========================================================
# LIVE CACHE (IN-MEMORY REAL TIME STORE)
# ==========================================================
class LiveCache:
    """
    Lightweight in-memory cache updated by daemon OR MCPStore sync.
    Includes a self-cleaning RAM log terminal stream capped strictly at 10MB.
    """

    _store = {
        "auth": [],
        "network": [],
        "security": [],
        "system": []
    }

    # Tracking for raw terminal logs streaming from daemon socket
    _terminal_logs = []
    _terminal_bytes = 0
    
    # Strict 10 MB RAM Ceiling limit in Bytes
    MAX_RAM_BYTES = 10 * 1024 * 1024 

    _last_update = 0

    @classmethod
    def push(cls, category: str, data: dict):
        if category not in cls._store:
            cls._store[category] = []

        cls._store[category].append(data)
        cls._last_update = time.time()

    @classmethod
    def push_terminal_log(cls, log_line: str):
        """
        Appends a log line to RAM and dynamically monitors its memory footprint.
        Triggers a 20% memory eviction if total usage reaches 10MB.
        """
        formatted_line = log_line if log_line.endswith("\n") else f"{log_line}\n"
        line_bytes = sys.getsizeof(formatted_line)

        # Enforce the 10MB threshold check
        if cls._terminal_bytes + line_bytes > cls.MAX_RAM_BYTES:
            # Calculate the target log items to drop to free up 20% of the maximum allocated space
            target_eviction_bytes = cls.MAX_RAM_BYTES * 0.20
            freed_bytes = 0
            evict_count = 0
            
            for line in cls._terminal_logs:
                freed_bytes += sys.getsizeof(line)
                evict_count += 1
                if freed_bytes >= target_eviction_bytes:
                    break
            
            # Splice out the old logs and update byte counter
            cls._terminal_logs = cls._terminal_logs[evict_count:]
            cls._terminal_bytes -= freed_bytes
            
            # Append a clean buffer rotation marker to the terminal trace
            rotation_msg = f"--- [SYSTEM] RAM Cache Limit Reached. Evicted oldest 20% ({evict_count} rows) ---\n"
            cls._terminal_logs.insert(0, rotation_msg)
            cls._terminal_bytes += sys.getsizeof(rotation_msg)

        cls._terminal_logs.append(formatted_line)
        cls._terminal_bytes += line_bytes
        cls._last_update = time.time()

    @classmethod
    def get_terminal_output(cls) -> str:
        """Returns the completely stitched in-RAM log stream."""
        return "".join(cls._terminal_logs)

    @classmethod
    def get_ram_usage_mb(cls) -> float:
        """Helper to get current log metrics directly on the dashboard UI."""
        return cls._terminal_bytes / (1024 * 1024)

    @classmethod
    def get(cls, category: str):
        return cls._store.get(category, [])

    @classmethod
    def get_all(cls):
        return cls._store

    @classmethod
    def clear(cls):
        cls._store = {"auth": [], "network": [], "security": [], "system": []}
        cls._terminal_logs = []
        cls._terminal_bytes = 0


# ==========================================================
# BACKGROUND IN-MEMORY SOCKET CONSUMER
# ==========================================================
def listen_to_daemon_socket():
    """Connects to daemon socket in RAM and streams log rows continuously."""
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(('127.0.0.1', 5555))
            buffer = ""
            while True:
                data = s.recv(4096).decode('utf-8', errors='ignore')
                if not data: 
                    break
                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    if line.strip():
                        LiveCache.push_terminal_log(line)
        except Exception:
            # Retry connection safely if daemon drops or hasn't booted up yet
            time.sleep(2)


# Register the persistent loop background listener once inside the session lifecycle
if "socket_started" not in st.session_state:
    st.session_state["socket_started"] = True
    threading.Thread(target=listen_to_daemon_socket, daemon=True).start()


# ==========================================================
# SYNC FROM DAEMON 
# ==========================================================
def sync_from_daemon():
    """
    REAL FLOW:
    Daemon → MCPStore (Supabase) → Dashboard Cache
    """
    try:
        from src.storage.mcp_store import MCPStore

        # pull latest tool logs (REAL DAEMON OUTPUT)
        for tool in ["auth", "network", "security", "system"]:
            records = MCPStore.get(tool)

            if records:
                for r in records:
                    LiveCache.push(tool, r)

    except Exception as e:
        # Gracefully handle sync exceptions without crashing UI thread
        pass


# ==========================================================
# AUTO SYNC (FAST LIGHTWEIGHT)
# ==========================================================
sync_from_daemon()


# ==========================================================
# TOOL INIT (ONLY IF NEEDED FOR DIRECT QUERY)
# ==========================================================
auth = AuthTools()
network = NetworkTools()
security = SecurityTools()
system = SystemTools()


# ==========================================================
# METRICS (FAST CACHE READ)
# ==========================================================
auth_logs = LiveCache.get("auth")
network_logs = LiveCache.get("network")
security_logs = LiveCache.get("security")
system_logs = LiveCache.get("system")


col1, col2, col3, col4 = st.columns(4)

col1.metric("Auth Events", len(auth_logs))
col2.metric("Network Events", len(network_logs))
col3.metric("Security Events", len(security_logs))
col4.metric("System Events", len(system_logs))

st.divider()


# ==========================================================
# ALERT ENGINE (GLOBAL DAEMON ALERTS)
# ==========================================================
st.subheader("🚨 Live Alerts")

alerts = GlobalAlertStore.get_latest() if hasattr(GlobalAlertStore, "get_latest") else []

if alerts:
    for alert in alerts[-5:]:
        st.error(f"⚠️ {alert.get('message', 'Anomaly detected')}")
else:
    st.success("System Stable (No Active Alerts)")


# ==========================================================
# EVENT FLOW GRAPH (MINIMAL FAST LINE CHART)
# ==========================================================
st.subheader("📈 Live Event Flow")

df = pd.DataFrame({
    "source": ["auth", "network", "security", "system"],
    "count": [
        len(auth_logs),
        len(network_logs),
        len(security_logs),
        len(system_logs)
    ]
})

st.line_chart(df.set_index("source"))


# ==========================================================
# LOG TABLES (FAST VIEW)
# ==========================================================
st.divider()

tab1, tab2, tab3, tab4 = st.tabs(
    ["Auth", "Network", "Security", "System"]
)

with tab1:
    st.dataframe(auth_logs, use_container_width=True)

with tab2:
    st.dataframe(network_logs, use_container_width=True)

with tab3:
    st.dataframe(security_logs, use_container_width=True)

with tab4:
    st.dataframe(system_logs, use_container_width=True)


# ==========================================================
# 💻 LIVE TERMINAL CONSOLE FEED (RAM BOUNDED)
# ==========================================================
st.divider()
st.subheader("💻 Live Splunk Daemon Console Feed")

# Diagnostic sub-caption displaying current allocated RAM consumption
st.caption(f"**In-Memory Buffer Telemetry:** Using **{LiveCache.get_ram_usage_mb():.4f} MB** / 10.0000 MB Max Capacity.")

# Output raw log array out of volatile volatile store structures
terminal_output = LiveCache.get_terminal_output()

if terminal_output:
    st.code(terminal_output, language="bash")
else:
    st.info("Awaiting terminal data socket handshake initialization...")


# ==========================================================
# LIVE AUTO REFRESH 
# ==========================================================
time.sleep(2)   # low latency refresh

st.rerun()