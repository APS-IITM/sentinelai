import streamlit as st
import pandas as pd
import plotly.express as px
import random 

from app_pages.ui_components.supabase_loader import (
    get_anomalies,
    get_intel_reports
)

# =========================
# PAGE CONFIG
# =========================
st.title("🛡️ SentinelAI SOC Command Center")
st.caption("Real-Time Multi-Domain Security Operations Dashboard (Auth • Network • System • Security)")
st.markdown("---")


# =========================
# DATA LAYER
# =========================
anomalies = get_anomalies()
intel_reports = get_intel_reports()

df = pd.DataFrame(anomalies) if anomalies else pd.DataFrame()


# =========================
# NORMALIZATION
# =========================
if not df.empty:
    if "severity" not in df.columns:
        df["severity"] = "LOW"
    if "attack_type" not in df.columns:
        df["attack_type"] = "UNKNOWN"
    if "source" not in df.columns:
        df["source"] = "SIMULATOR"


# =========================
# METRICS STRIP
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Events", len(df))

critical = len(df[df["severity"] == "CRITICAL"]) if not df.empty else 0
col2.metric("Critical Events", critical)

col3.metric("Intel Reports", len(intel_reports) if intel_reports else 0)

attack_types = df["attack_type"].nunique() if not df.empty else 0
col4.metric("Attack Vectors Active", attack_types)

st.markdown("---")


# =========================
# LIVE INCIDENT FEED
# =========================
st.subheader("🚨 Live SOC Incident Feed")

if df.empty:
    st.info("No active incidents in SOC pipeline.")
else:
    st.dataframe(
        df.sort_values(by=df.columns[0], ascending=False),
        use_container_width=True
    )

st.markdown("---")


# =========================
# 📊 SOC ANALYTICS ENGINE
# =========================
if not df.empty:
    st.subheader("📊 SOC Analytics Overview")

    # PIE: Severity Distribution
    sev = df["severity"].value_counts().reset_index()
    sev.columns = ["severity", "count"]

    fig_pie = px.pie(
        sev,
        names="severity",
        values="count",
        title="Threat Severity Distribution",
        color_discrete_sequence=px.colors.sequential.Agsunset
    )
    st.plotly_chart(fig_pie, use_container_width=True)

    # BAR: Attack Type Distribution
    atk = df["attack_type"].value_counts().reset_index()
    atk.columns = ["attack_type", "count"]

    fig_bar = px.bar(
        atk,
        x="attack_type",
        y="count",
        text="count",
        title="Attack Vector Distribution",
        color="attack_type"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # LINE: Incident Trend
    if "created_at" in df.columns:
        df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
        trend_df = df.dropna(subset=["created_at"])

        trend = trend_df.groupby(trend_df["created_at"].dt.date).size().reset_index(name="count")
        trend.columns = ["date", "count"]

        fig_line = px.line(
            trend,
            x="date",
            y="count",
            markers=True,
            title="Incident Trend Timeline"
        )
        st.plotly_chart(fig_line, use_container_width=True)


# =========================
# INTELLIGENCE SNAPSHOT (FIXED: RANDOM 4 SELECT MAX)
# =========================
st.subheader("🧠 Intelligence Snapshot")

if intel_reports:
    # Safe range check sample selection
    sample_size = min(len(intel_reports), 4)
    sampled_snapshots = random.sample(intel_reports, sample_size)

    for r in sampled_snapshots:
        st.markdown(f"""
        <div class="card" style="margin-bottom: 12px;">
            <h4>Incident: {r.get('incident_type', 'UNKNOWN')}</h4>
            <p><b>Severity:</b> {r.get('severity', 'N/A')}</p>
            <p style="color:#555;">{r.get('attack_story', 'No narrative available')}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No intelligence reports available.")


# =========================
# SOC PIPELINE VIEW
# =========================
st.markdown("---")
st.markdown("""
### 🧬 SOC Pipeline Flow
Attack Simulator → MCP Layer (Auth / Network / System / Security) → Splunk Queries → Anomaly Engine → Intelligence Engine → AI Analysis Layer
""")