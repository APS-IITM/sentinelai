import streamlit as st

def apply_theme():
    st.markdown("""
    <style>
    .stApp {
        background-color: #FAFAFA;
        color: #111;
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
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 12px rgba(0,0,0,0.06);
        border: 1px solid #eee;
    }

    h1, h2, h3 {
        font-family: Inter;
        font-weight: 500;
    }
    </style>
    """, unsafe_allow_html=True)