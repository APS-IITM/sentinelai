import streamlit as st
import time

# 1. Page Settings (Must be the absolute first Streamlit command)
st.set_page_config(
    page_title="SentinelAI - Incident Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject your exact global aesthetic CSS plus custom splash architecture
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&display=swap');

/* Dynamic Splash Cover Layer */
#splash-container {
    position: fixed;
    top: 0; left: 0; width: 100vw; height: 100vh;
    background: #FAFAFA;
    z-index: 9999999;
    display: flex; flex-direction: column; justify-content: center; align-items: center;
    animation: smoothExit 2.2s cubic-bezier(0.25, 1, 0.5, 1) forwards;
    pointer-events: none;
}
.premium-loader {
    width: 60px; height: 60px;
    border: 2px solid #EAEAEA;
    border-top: 2px solid #D4AF37;
    border-radius: 50%;
    animation: velocitySpin 1.2s cubic-bezier(0.4, 0, 0.2, 1) infinite;
}
@keyframes velocitySpin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
@keyframes smoothExit { 0% { opacity: 1; } 80% { opacity: 1; } 100% { opacity: 0; visibility: hidden; } }

/* Global Light-Premium Elements Framework Override */
.stApp {
    background-color: #FAFAFA;
    color: #111111;
    font-family: 'Inter', sans-serif;
}
div[data-testid="stMetric"] {
    background: white;
    border-radius: 10px;
    padding: 18px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    border: 1px solid #eee;
}
.card {
    background: white;
    padding: 24px;
    border-radius: 12px;
    box-shadow: 0 2px 12px rgba(0,0,0,0.06);
    border: 1px solid #eee;
    margin-bottom: 20px;
    transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,0,0,0.08);
    border-color: #D4AF37;
}
.card h4 { margin: 0 0 6px 0; color: #666666; font-size: 13px; font-weight: 500; text-transform: uppercase; letter-spacing: 0.5px; }
.card h2 { margin: 0 0 4px 0; color: #111111; font-size: 34px; font-weight: 600; }
.card small { color: #00B074; font-weight: 500; font-size: 13px; }

/* Interactive Premium Menu Block Items */
.nav-block-card {
    background: #FFFFFF;
    border: 1px solid #EAEAEA;
    padding: 20px;
    border-radius: 10px;
    cursor: pointer;
    text-align: center;
    transition: all 0.2s ease;
}
.nav-block-card:hover {
    background: #FAF6E8;
    border-color: #D4AF37;
}

/* Button Theming Override */
.stButton>button {
    background-color: #FFFFFF; color: #111111;
    border: 1px solid #EAEAEA; border-radius: 6px;
    padding: 8px 18px; font-weight: 500; transition: all 0.25s ease;
}
.stButton>button:hover {
    border-color: #D4AF37; background-color: #FAF6E8; color: #D4AF37;
}
</style>

<div id="splash-container">
    <div class="premium-loader"></div>
    <h2 style="font-family:'Inter'; font-weight:400; margin-top:24px; color:#111; letter-spacing:2px;">SENTINELAI</h2>
    <p style="font-family:'Inter'; color:#888; font-size:12px; letter-spacing:0.5px;">SECURE INTELLIGENCE INTERFACE</p>
</div>
""", unsafe_allow_html=True)

# 3. Dynamic Application Directory Layout Allocation
pages = {
    "📊 Monitoring": [
        st.Page("app_pages/dashboard.py", title="Dashboard Summary"),
        st.Page("app_pages/threat_monitor.py", title="Threat Monitor"),
    ],
    "🧠 Intelligence": [
        st.Page("app_pages/intelligence_center.py", title="CTI Engine"),
        st.Page("app_pages/ai_reports.py", title="AI Reports Workspace"),
    ],
    "🧰 Forensics": [
        st.Page("app_pages/investigation.py", title="Investigation Console"),
        st.Page("app_pages/settings.py", title="Settings Panel"),
    ]
}

nav = st.navigation(pages)
nav.run()