import streamlit as st
import asyncio
from src.alerts.global_alerts import GlobalAlertStore

st.set_page_config(page_title="Global Alerts", layout="wide")

st.title("🚨 SentinelAI Global Alerts")

alerts = asyncio.run(GlobalAlertStore.get_alerts(100))

if not alerts:
    st.info("No active alerts")
else:
    for alert in alerts:
        severity = alert.get("severity", "LOW")

        color = {
            "CRITICAL": "🔴",
            "HIGH": "🟠",
            "MEDIUM": "🟡",
            "LOW": "🟢"
        }.get(severity, "⚪")

        st.markdown(f"""
        ### {color} {alert.get("title")}

        - **Severity:** {severity}
        - **Type:** {alert.get("attack_type")}
        - **Summary:** {alert.get("summary")}
        - **Events:** {alert.get("source_events")}
        - **Time:** {alert.get("timestamp")}
        """)