import streamlit as st
import pandas as pd
import plotly.express as px

from app_pages.ui_components.supabase_loader import (
    get_anomalies,
    get_intel_reports
)

# =========================
# PAGE HEADER
# =========================
st.title("🛡️ SentinelAI SOC Command Center")
st.caption("Unified Security Intelligence | Real-Time Threat Visibility | AI Driven SOC Operations")
st.markdown("---")


# =========================
# DATA LAYER
# =========================
anomalies = get_anomalies()
intel_reports = get_intel_reports()

df = pd.DataFrame(anomalies) if anomalies else pd.DataFrame()


# =========================
# SOC HEALTH SCORE ENGINE (NEW)
# =========================
def compute_soc_health(df):

    if df.empty:
        return 100

    score = 100

    if "severity" in df.columns:
        high = len(df[df["severity"].astype(str).str.upper() == "HIGH"])
        score -= high * 8

    if len(df) > 50:
        score -= 10

    return max(0, min(100, score))


soc_health = compute_soc_health(df)


# =========================
# TOP SOC METRICS STRIP
# =========================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("SOC Health Score", f"{soc_health}/100")

with col2:
    st.metric("Active Anomalies", len(df) if not df.empty else 0)

with col3:
    st.metric("Intelligence Reports", len(intel_reports) if intel_reports else 0)

with col4:
    attack_state = "ACTIVE" if len(df) > 0 else "STABLE"
    st.metric("Threat State", attack_state)


st.markdown("---")


# =========================
# LIVE THREAT OVERVIEW (SOC GLASS PANEL)
# =========================
st.markdown("### 🚨 Live Threat Overview")

if df.empty:
    st.info("No active anomalies detected. System currently in stable monitoring state.")

else:
    display_df = df.copy()

    if "created_at" in display_df.columns:
        display_df["created_at"] = pd.to_datetime(display_df["created_at"], errors="coerce")

    st.dataframe(display_df, use_container_width=True)


st.markdown("---")


# =========================
# SEVERITY DISTRIBUTION (SOC VISUALIZATION)
# =========================
if not df.empty and "severity" in df.columns:

    st.markdown("### 📊 Threat Severity Distribution")

    sev = df["severity"].value_counts().reset_index()
    sev.columns = ["severity", "count"]

    fig = px.bar(
        sev,
        x="severity",
        y="count",
        color="severity",
        text="count"
    )

    fig.update_layout(
        plot_bgcolor="white",
        paper_bgcolor="white",
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)


# =========================
# INTELLIGENCE SNAPSHOT (NEW SOC LAYER)
# =========================
st.markdown("### 🧠 Intelligence Snapshot")

if intel_reports:

    latest = intel_reports[:5]

    for r in latest:

        st.markdown(f"""
        <div class="card">
            <h4>Incident Type: {r.get('incident_type', 'UNKNOWN')}</h4>
            <p><b>Severity:</b> {r.get('severity', 'N/A')}</p>
            <p style="color:#555;">{r.get('attack_story', 'No narrative available')}</p>
        </div>
        """, unsafe_allow_html=True)

else:
    st.info("No intelligence reports generated yet.")


# =========================
# SOC PIPELINE STATUS PANEL (NEW)
# =========================
st.markdown("---")

st.markdown("### 🧬 SOC Pipeline Status")

st.markdown("""
<div class="card">

<b>Attack Flow:</b><br>
🟥 Attack Simulator → 🟧 MCP Tools → 🟨 Splunk Queries → 🟩 Anomaly Engine → 🟦 Intelligence Engine → 🤖 AI Layer

<hr>

<b>Current Mode:</b> Real-time Security Simulation Engine<br>
<b>Processing:</b> Event-driven log correlation<br>
<b>AI Layer:</b> Gemini-powered incident reasoning

</div>
""", unsafe_allow_html=True)