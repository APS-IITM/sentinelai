import streamlit as st
import pandas as pd
import plotly.express as px
import random

import main

st.title("🛡️ SentinelAI SOC Command Center")
st.caption("Real-Time Multi-Domain Security Operations Dashboard")
st.markdown("---")


anomalies = main.get_all_anomalies()
intel_reports = main.get_all_intelligence_reports()

df = pd.DataFrame(anomalies) if anomalies else pd.DataFrame()

if not df.empty:
    if "severity" not in df.columns:
        df["severity"] = "LOW"
    if "attack_type" not in df.columns:
        df["attack_type"] = "UNKNOWN"
    if "source" not in df.columns:
        df["source"] = "SIMULATOR"


col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Events", len(df))
critical = len(df[df["severity"] == "CRITICAL"]) if not df.empty else 0
col2.metric("Critical Events", critical)
col3.metric("Intel Reports", len(intel_reports) if intel_reports else 0)
attack_types = df["attack_type"].nunique() if not df.empty else 0
col4.metric("Attack Vectors Active", attack_types)

st.markdown("---")

st.subheader("🚨 Live SOC Incident Feed")

if df.empty:
    st.info("No active incidents.")
else:
    st.dataframe(df, use_container_width=True)

st.markdown("---")

st.subheader("📊 SOC Analytics Overview")

if not df.empty:
    sev = df["severity"].value_counts().reset_index()
    sev.columns = ["severity", "count"]

    fig = px.pie(sev, names="severity", values="count")
    st.plotly_chart(fig, use_container_width=True)

    atk = df["attack_type"].value_counts().reset_index()
    atk.columns = ["attack_type", "count"]

    fig2 = px.bar(atk, x="attack_type", y="count", text="count")
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")

st.subheader("🧠 Intelligence Snapshot")

if intel_reports:
    sample = random.sample(intel_reports, min(len(intel_reports), 4))
    for r in sample:
        st.markdown(f"""
        <div class="card">
            <h4>{r.get('incident_type')}</h4>
            <p>{r.get('attack_story')}</p>
        </div>
        """, unsafe_allow_html=True)