import streamlit as st
import time

# Config
st.set_page_config(
    page_title="SentinelAI - Incident Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Premium Global Light Theme CSS & Splash Screen Animation
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

/* Splash Screen Setup */
#splash-screen {
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    background: #FFFFFF;
    z-index: 999999;
    display: flex; flex-direction: column; justify-content: center; align-items: center;
    animation: fadeOut 1.8s ease-in-out forwards;
    pointer-events: none;
}
.spinner {
    width: 50px; height: 50px;
    border: 3px solid #EAEAEA;
    border-top: 3px solid #D4AF37;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}
@keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
@keyframes fadeOut { 0% { opacity: 1; } 85% { opacity: 1; } 100% { opacity: 0; visibility: hidden; } }

/* App Structural Adjustments */
.stApp { background-color: #FAFAFA; color: #111111; font-family: 'Inter', sans-serif; }

/* Custom Premium Components */
.card {
    background: #FFFFFF;
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.03);
    border: 1px solid #EDEDED;
    margin-bottom: 20px;
    transition: transform 0.2s ease;
}
.card:hover { transform: translateY(-2px); }
.card h4 { margin: 0 0 8px 0; color: #666666; font-size: 14px; font-weight: 400; text-transform: uppercase; letter-spacing: 0.5px; }
.card h2 { margin: 0 0 4px 0; color: #111111; font-size: 32px; font-weight: 600; }
.card small { color: #00B074; font-weight: 500; }

/* Navigation & Button overrides */
.stButton>button {
    background-color: #FFFFFF; color: #111111;
    border: 1px solid #E0E0E0; border-radius: 6px;
    padding: 8px 16px; font-weight: 500; transition: all 0.3s;
}
.stButton>button:hover {
    border-color: #D4AF37; background-color: #FAF6E8; color: #D4AF37;
}
</style>

<div id="splash-screen">
    <div class="spinner"></div>
    <h2 style="font-family:'Inter'; font-weight:400; margin-top:20px; color:#111; letter-spacing:1px;">SENTINELAI</h2>
    <p style="font-family:'Inter'; color:#888; font-size:12px;">Initializing secure perimeter...</p>
</div>
""", unsafe_allow_html=True)

# Navigation Definitions pointing to app_pages/
pages = {
    "📊 Monitoring": [
        st.Page("app_pages/dashboard.py", title="Dashboard"),
        st.Page("app_pages/threat_monitor.py", title="Threat Monitor"),
    ],
    "🧠 Intelligence": [
        st.Page("app_pages/intelligence_center.py", title="CTI Engine"),
        st.Page("app_pages/ai_reports.py", title="AI Reports"),
    ],
    "🧰 Forensics": [
        st.Page("app_pages/investigation.py", title="Investigation Console"),
        st.Page("app_pages/settings.py", title="Settings"),
    ]
}

nav = st.navigation(pages)
nav.run()