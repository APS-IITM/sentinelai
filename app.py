import os
import sys
import subprocess
import streamlit as st

from app_pages.ui_components.theme import apply_theme
from app_pages.splash import show_splash


# =====================================================
# BACKGROUND SOC DAEMON
# =====================================================
@st.cache_resource
def start_background_soc_daemon():

    base_dir = os.path.dirname(os.path.abspath(__file__))

    daemon_script = os.path.join(
        base_dir,
        "src",
        "anomaly",
        "splunk_daemon.py"
    )

    if not os.path.exists(daemon_script):
        print(f"[SentinelAI] Daemon not found: {daemon_script}")
        return False

    try:

        subprocess.Popen(
            [sys.executable, daemon_script],
            env=os.environ,
            start_new_session=True
        )

        print("[SentinelAI] SOC daemon started")

        return True

    except Exception as e:

        print(f"[SentinelAI] Failed to start daemon: {e}")

        return False


# Start backend once
start_background_soc_daemon()


# =====================================================
# PAGE CONFIG
# =====================================================
st.set_page_config(
    page_title="SentinelAI SOC",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_theme()


# =====================================================
# SPLASH SCREEN
# =====================================================
if "splash_done" not in st.session_state:

    show_splash()

    st.session_state.splash_done = True


# =====================================================
# NAVIGATION
# =====================================================
pages = {

    "🛡️ SOC Command Center": [
        st.Page(
            "app_pages/dashboard.py",
            title="SOC Home"
        ),
    ],

    "📊 Monitoring": [
        st.Page(
            "app_pages/threat_monitor.py",
            title="Threat Monitor"
        ),
    ],

    "🟥 War Room": [
        st.Page(
            "app_pages/soc_war_room.py",
            title="Attack Simulator"
        ),
    ],

    "🧠 Intelligence": [

        st.Page(
            "app_pages/intelligence_center.py",
            title="CTI Engine"
        ),

        st.Page(
            "app_pages/ai_reports.py",
            title="AI Reports"
        ),
    ],

    "🧰 Forensics": [
        st.Page(
            "app_pages/investigation.py",
            title="Investigation Console"
        ),
    ],

    "⚙️ Settings": [
        st.Page(
            "app_pages/settings.py",
            title="System Config"
        ),
    ],
}


# =====================================================
# RENDER APP
# =====================================================
navigation = st.navigation(pages)
navigation.run()