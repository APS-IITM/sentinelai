import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import random

from app_pages.ui_components.supabase_loader import get_anomalies, get_intel_reports


# =========================
# PAGE HEADER
# =========================
st.title("🛡️ SentinelAI SOC Command Center")
st.caption("Real-Time Security Operations Dashboard | AI Driven Threat Intelligence")
st.markdown("---")


# =========================
# DATA
# =========================
anomalies = get_anomalies()
intel_reports = get_intel_reports()

df = pd.DataFrame(anomalies) if anomalies else pd.DataFrame()


# =========================
# SOC HEALTH ENGINE
# =========================
def soc_health_score(df):
    score = 100

    if not df.empty and "severity" in df.columns:
        high = len(df[df["severity"].astype(str).str.upper() == "HIGH"])
        critical = len(df[df["severity"].astype(str).str.upper() == "CRITICAL"])
        score -= (high * 8 + critical * 15)

    if len(df) > 50:
        score -= 10

    return max(0, min(100, score))


health = soc_health_score(df)


# =========================
# METRICS
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("SOC Health", f"{health}/100")
col2.metric("Active Anomalies", len(df))
col3.metric("Intel Reports", len(intel_reports) if intel_reports else 0)

state = "ACTIVE" if len(df) > 0 else "STABLE"
col4.metric("Threat State", state)


st.markdown("---")


# =========================
# LIVE TABLE
# =========================
st.subheader("🚨 Live Incident Feed")

if df.empty:
    st.info("No active threats detected. SOC is stable.")
else:
    st.dataframe(df, use_container_width=True)


st.markdown("---")


# =========================
# 📊 MULTI-CHART SOC VIEW (IMPORTANT UPGRADE)
# =========================

if not df.empty and "severity" in df.columns:

    st.subheader("📊 SOC Analytics Overview")

    # ---- PIE CHART ----
    pie_data = df["severity"].value_counts().reset_index()
    pie_data.columns = ["severity", "count"]

    fig_pie = px.pie(
        pie_data,
        names="severity",
        values="count",
        title="Threat Distribution (Pie)"
    )

    st.plotly_chart(fig_pie, use_container_width=True)


    # ---- BAR CHART ----
    fig_bar = px.bar(
        pie_data,
        x="severity",
        y="count",
        text="count",
        color="severity",
        title="Severity Breakdown (Bar)"
    )

    st.plotly_chart(fig_bar, use_container_width=True)


    # ---- LINE CHART (TREND SIMULATION) ----
    trend_df = df.copy()
    if "created_at" in trend_df.columns:
        trend_df["created_at"] = pd.to_datetime(trend_df["created_at"], errors="coerce")
        trend_df = trend_df.dropna(subset=["created_at"])

        trend = trend_df.groupby(trend_df["created_at"].dt.date).size().reset_index(name="count")
        trend.columns = ["date", "count"]

        fig_line = px.line(
            trend,
            x="date",
            y="count",
            title="Incident Trend Over Time"
        )

        st.plotly_chart(fig_line, use_container_width=True)


# =========================
# INTELLIGENCE SNAPSHOT
# =========================
st.subheader("🧠 Intelligence Snapshot")

if intel_reports:
    for r in intel_reports[:5]:
        st.markdown(f"""
        <div class="card">
            <h4>{r.get('incident_type', 'UNKNOWN')}</h4>
            <p><b>Severity:</b> {r.get('severity', 'N/A')}</p>
            <p>{r.get('attack_story', '')}</p>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No intelligence reports yet.")


# =========================
# PIPELINE VIEW
# =========================
st.markdown("---")

st.markdown("""
### 🧬 SOC Pipeline Flow

Attack Simulator → MCP Tools → Splunk Queries → Anomaly Engine → Intelligence Layer → AI Analysis
""")