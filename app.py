import streamlit as st

from app_pages.ui_components.theme import apply_theme
from app_pages.splash import show_splash


# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="SentinelAI SOC",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_theme()


# =========================
# SPLASH CONTROL (FIXED: NO RERUN CRASH)
# =========================
if "splash_done" not in st.session_state:
    show_splash()
    st.session_state.splash_done = True
    # Let the script continue execution into st.navigation naturally


# =========================
# MAIN SOC NAVIGATION SYSTEM
# =========================
pages = {
    "🛡️ SOC Command Center": [
        st.Page("app_pages/dashboard.py", title="SOC Home"),
    ],
    "📊 Monitoring": [
        st.Page("app_pages/threat_monitor.py", title="Threat Monitor"),
    ],
    "🟥 War Room": [
        st.Page("app_pages/soc_war_room.py", title="Attack Simulator"),
    ],
    "🧠 Intelligence": [
        st.Page("app_pages/intelligence_center.py", title="CTI Engine"),
        st.Page("app_pages/ai_reports.py", title="AI Reports"),
    ],
    "🧰 Forensics": [
        st.Page("app_pages/investigation.py", title="Investigation Console"),
    ],
    "⚙️ Settings": [
        st.Page("app_pages/settings.py", title="System Config"),
    ],
}


# =========================
# SOC NAVIGATION RENDER
# =========================
nav = st.navigation(pages)
nav.run()