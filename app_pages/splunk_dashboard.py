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

from src.alerts.global_alerts import GlobalAlertStore
from main import get_soc_snapshot, get_anomaly_source_distribution, get_all_anomalies

# ==========================================================
# PAGE CONFIG
# ==========================================================
st.set_page_config(
    page_title="SentinelAI Splunk Live Dashboard",
    layout="wide",
)

st.title("⚙️ SentinelAI Splunk Live Stream")
st.caption("Real-time MCP → Splunk → Daemon → Alert Pipeline")
st.divider()

MAX_RAM_BYTES    = 10 * 1024 * 1024
MAX_RENDER_LINES = 250

# ==========================================================
# SESSION STATE BOOTSTRAP
# ==========================================================
defaults = {
    "terminal_logs":  [],
    "terminal_bytes": 0,
    "socket_started": False,
    # Rolling history for the line chart (one dict per cycle)
    "chart_history":  [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ==========================================================
# THREAD-SAFE LOG PUSH
# ==========================================================
_log_lock = threading.Lock()


def push_log(line: str):
    """Append a log line to session state, evicting oldest 20% at RAM ceiling."""
    formatted  = line.strip() + "\n"
    line_bytes = sys.getsizeof(formatted)

    with _log_lock:
        if st.session_state["terminal_bytes"] + line_bytes > MAX_RAM_BYTES:
            target = MAX_RAM_BYTES * 0.20
            freed, count = 0, 0
            for old in st.session_state["terminal_logs"]:
                freed += sys.getsizeof(old)
                count += 1
                if freed >= target:
                    break

            st.session_state["terminal_logs"]  = st.session_state["terminal_logs"][count:]
            st.session_state["terminal_bytes"] -= freed

            notice = f"--- [SYSTEM] RAM ceiling hit — evicted {count} oldest lines ---\n"
            st.session_state["terminal_logs"].insert(0, notice)
            st.session_state["terminal_bytes"] += sys.getsizeof(notice)

        st.session_state["terminal_logs"].append(formatted)
        st.session_state["terminal_bytes"] += line_bytes


# ==========================================================
# SOCKET CLIENT (dashboard connects TO daemon's server)
# ==========================================================
def _socket_reader_thread():
    """
    Connects to SplunkDaemon's TCP log server as a CLIENT.
    Auto-reconnects with 3s backoff if daemon restarts.
    """
    while True:
        sock = None
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("127.0.0.1", 5555))
            push_log("[DASHBOARD] Connected to SplunkDaemon log stream on :5555")

            buffer = ""
            while True:
                data = sock.recv(4096)
                if not data:
                    push_log("[DASHBOARD] Daemon closed connection — reconnecting...")
                    break

                buffer += data.decode("utf-8", errors="ignore")

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if line:
                        push_log(line)

                if len(buffer) > 500:
                    push_log(buffer[:500])
                    buffer = buffer[500:]

        except ConnectionRefusedError:
            push_log("[DASHBOARD] Daemon not reachable on :5555 — retrying in 3s...")
        except Exception as e:
            push_log(f"[DASHBOARD] Socket error: {e} — retrying in 3s...")
        finally:
            if sock:
                try:
                    sock.close()
                except Exception:
                    pass
        time.sleep(3)


if not st.session_state["socket_started"]:
    st.session_state["socket_started"] = True
    threading.Thread(target=_socket_reader_thread, daemon=True).start()


# ==========================================================
# DATA FETCH  (single snapshot, reused by all UI sections)
# ==========================================================
snapshot = get_soc_snapshot()
metrics  = snapshot["metrics"]
src_dist = snapshot["source_distribution"]   # % per source bucket from anomalies

# Append current distribution to rolling chart history (max 60 cycles ≈ 10 min)
st.session_state["chart_history"].append(src_dist)
if len(st.session_state["chart_history"]) > 60:
    st.session_state["chart_history"].pop(0)

# ==========================================================
# UI — METRICS ROW
# ==========================================================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Anomalies",      metrics["total_anomalies"])
col2.metric("Intelligence Reports", metrics["total_intelligence"])
col3.metric("AI Reports",           metrics["total_ai_reports"])

dominant = max(src_dist, key=src_dist.get) if any(src_dist.values()) else "none"
col4.metric("Top Attack Source", dominant.upper(), f"{src_dist.get(dominant, 0):.1f}%")

st.divider()

# ==========================================================
# UI — LIVE ALERTS
# ==========================================================
st.subheader("🚨 Live Alerts")

try:
    alerts = GlobalAlertStore.get_latest() if hasattr(GlobalAlertStore, "get_latest") else []
except Exception:
    alerts = []

if alerts:
    for alert in reversed(alerts[-5:]):
        severity   = str(alert.get("severity", "MEDIUM")).upper()
        title      = alert.get("title", "Anomaly detected")
        attack     = alert.get("attack_type", "unknown")
        summary    = alert.get("summary", "")
        src_events = alert.get("source_events", "?")
        render     = st.error if severity in ("HIGH", "CRITICAL") else st.warning
        render(f"⚠️ [{severity}] {title} — {attack} | {src_events} events | {summary}")
else:
    st.success("✅ System Stable — No Active Alerts")

st.divider()

# ==========================================================
# UI — ANOMALY SOURCE % LINE CHART
# Y-axis = % of total anomalies detected by that source bucket.
# X-axis = daemon cycles (one point per 10s rerun).
# Grows up to 60 cycles (~10 minutes) then rolls.
# ==========================================================
st.subheader("📈 Anomaly Source Distribution (% per source over time)")

if st.session_state["chart_history"]:
    chart_df = pd.DataFrame(st.session_state["chart_history"])

    # Ensure all four columns exist even if a source had 0% this cycle
    for col in ["auth", "network", "security", "system"]:
        if col not in chart_df.columns:
            chart_df[col] = 0.0

    chart_df = chart_df[["auth", "network", "security", "system"]]
    chart_df.index.name = "cycle"

    st.line_chart(chart_df, use_container_width=True, height=300)
    st.caption(
        "Each line = one source bucket. Y-axis = % share of total anomalies "
        "detected by that source. One point added per 10-second daemon cycle."
    )

    # Current cycle breakdown as a quick reference row
    dist_col1, dist_col2, dist_col3, dist_col4 = st.columns(4)
    dist_col1.metric("Auth %",     f"{src_dist.get('auth', 0):.1f}%")
    dist_col2.metric("Network %",  f"{src_dist.get('network', 0):.1f}%")
    dist_col3.metric("Security %", f"{src_dist.get('security', 0):.1f}%")
    dist_col4.metric("System %",   f"{src_dist.get('system', 0):.1f}%")
else:
    st.info("📊 Waiting for anomaly data to build the chart...")

st.divider()

# ==========================================================
# UI — LATEST THREATS TABLE
# ==========================================================
st.subheader("🔍 Latest Threats")
latest_threats = snapshot["latest_threats"]
if latest_threats:
    threat_df    = pd.DataFrame(latest_threats)
    display_cols = [c for c in ["timestamp", "source", "attack_type", "severity", "score"]
                    if c in threat_df.columns]
    st.dataframe(
        threat_df[display_cols] if display_cols else threat_df,
        use_container_width=True,
    )
else:
    st.info("No threat records yet.")

st.divider()

# ==========================================================
# UI — LIVE TERMINAL CONSOLE
# ==========================================================
st.subheader("💻 Live Splunk Daemon Console Feed")

used_mb = st.session_state["terminal_bytes"] / (1024 * 1024)
st.caption(
    f"In-memory buffer: **{used_mb:.4f} MB** / 10.00 MB  |  "
    f"Lines buffered: **{len(st.session_state['terminal_logs'])}**"
)

with _log_lock:
    logs_snapshot = list(st.session_state["terminal_logs"])

terminal_output = "".join(logs_snapshot[-MAX_RENDER_LINES:])

if terminal_output.strip():
    st.code(terminal_output, language="bash")
else:
    st.info("🔄 Connecting to SplunkDaemon on :5555 — waiting for first log burst...")

# ==========================================================
# AUTO-RERUN every 10s (matches daemon poll interval)
# ==========================================================
time.sleep(10)
st.rerun()