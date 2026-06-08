import streamlit as st

# 1. Page Configuration (Must be first)
st.set_page_config(
    page_title="SentinelAI - Incident Intelligence",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject Premium Light Theme CSS Customizations
st.markdown("""
    <style>
    /* Global Background and Typography */
    .stApp { background-color: #FAFAFA; color: #1C1C1C; }
    
    /* Card/Container styling with soft diffuse shadows */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #EAEAEA;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02);
    }
    
    /* Premium accents */
    h1, h2, h3 { color: #1C1C1C; font-weight: 500; }
    .stButton>button {
        background-color: #FFFFFF;
        color: #1C1C1C;
        border: 1px solid #D4AF37 !important;
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #D4AF37 !important;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Define Page Routers using modern st.Page API
pages = {
    "Operations": [
        st.Page("app/dashboard.py", title="Dashboard", icon="✨"),
        st.Page("app/threat_monitor.py", title="Threat Monitor", icon="🔍"),
        st.Page("app/intelligence_center.py", title="Intelligence Center", icon="🧭"),
    ],
    "Analysis & Tools": [
        st.Page("app/ai_reports.py", title="AI Incident Reports", icon="🧠"),
        st.Page("app/investigation.py", title="Investigation Console", icon="🧰"),
        st.Page("app/settings.py", title="Settings", icon="⚙️"),
    ]
}

# 4. Render Navigation
pg = st.navigation(pages)

# Mock global session state data for the demo
if "selected_incident" not in st.session_state:
    st.session_state.selected_incident = "INC-2026-8841"

pg.run()