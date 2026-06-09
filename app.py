import streamlit as st
import time

from app_pages.ui_components.theme import apply_theme

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="SentinelAI SOC Command Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_theme()


# =========================
# SPLASH (KEEP YOUR STYLE)
# =========================
st.markdown("""
<div id="splash-container">
    <div class="premium-loader"></div>
    <h2 style="font-family:Inter; font-weight:400; margin-top:24px; color:#111; letter-spacing:2px;">
        SENTINELAI
    </h2>
    <p style="font-family:Inter; color:#888; font-size:12px;">
        SOC COMMAND OPERATIONS CENTER
    </p>
</div>
""", unsafe_allow_html=True)

time.sleep(1.2)


# =========================
# HEADER SOC STATUS BAR
# =========================
st.title("🛡️ SentinelAI SOC Command Center")
st.caption("Unified Cyber Defense & Attack Simulation Intelligence System")

st.markdown("---")


# =========================
# LIVE SOC METRICS STRIP
# =========================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("System Status", "OPERATIONAL", "Stable")

with col2:
    st.metric("Active Threats", "3", "+1")

with col3:
    st.metric("Attack Simulations", "Running", "Live Mode")

with col4:
    st.metric("AI Engine", "ONLINE", "Gemini Active")


st.markdown("---")


# =========================
# SOC COMMAND DASHBOARD (CARD NAVIGATION - NO BUTTON STYLE)
# =========================
st.markdown("### 🧭 SOC Command Matrix")


def soc_card(title, desc, page, color):
    st.markdown(f"""
    <a href="{page}" target="_self" style="text-decoration:none;">
        <div class="card" style="cursor:pointer; border-left:4px solid {color};">
            <h3 style="margin-bottom:6px;">{title}</h3>
            <p style="color:#666; margin:0;">{desc}</p>
        </div>
    </a>
    """, unsafe_allow_html=True)


col1, col2, col3 = st.columns(3)

with col1:
    soc_card(
        "🛡️ Threat Monitor",
        "Live security telemetry stream & incident tracking",
        "app_pages/threat_monitor.py",
        "#D4AF37"
    )

with col2:
    soc_card(
        "🟥 SOC War Room",
        "Attack simulation & control center",
        "app_pages/soc_war_room.py",
        "#AA820A"
    )

with col3:
    soc_card(
        "🧠 Intelligence Engine",
        "Threat correlation & attack story builder",
        "app_pages/intelligence_center.py",
        "#444444"
    )


col4, col5, col6 = st.columns(3)

with col4:
    soc_card(
        "🤖 AI Reports",
        "Gemini-powered incident analysis",
        "app_pages/ai_reports.py",
        "#777777"
    )

with col5:
    soc_card(
        "🧰 Forensics Console",
        "Deep log investigation engine",
        "app_pages/investigation.py",
        "#555555"
    )

with col6:
    soc_card(
        "⚙️ System Config",
        "SIEM + API configuration layer",
        "app_pages/settings.py",
        "#999999"
    )


st.markdown("---")


# =========================
# SOC OVERVIEW INSIGHT PANEL
# =========================
st.markdown("### 🧠 SOC Operational Overview")

st.markdown("""
<div class="card">
    <h4>SentinelAI Operational Flow</h4>

    <p style="color:#333;">
    Attack Simulation → MCP Tooling → Splunk Pipeline → Anomaly Detection →
    Intelligence Correlation → AI Incident Narrative
    </p>

    <hr>

    <p style="color:#666;">
    This system simulates a real-world Security Operations Center (SOC)
    with full attack lifecycle visibility and AI-assisted analysis.
    </p>
</div>
""", unsafe_allow_html=True)


st.markdown("---")


# =========================
# FOOTER STATUS
# =========================
st.caption("SentinelAI SOC System v1.0 | Hackathon Intelligence Platform | Real-Time Cyber Simulation Engine")