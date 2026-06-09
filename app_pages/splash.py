import streamlit as st
import time

def show_splash():
    splash = st.empty()

    with splash.container():
        st.markdown("""
        <style>
        .center {
            text-align:center;
            padding-top:20vh;
            animation: fadeIn 1.5s ease-in;
        }

        @keyframes fadeIn {
            0% {opacity:0;}
            100% {opacity:1;}
        }

        .title {
            font-size:40px;
            font-weight:600;
            color:#111;
        }

        .sub {
            color:#666;
            font-size:16px;
        }
        </style>

        <div class="center">
            <div class="title">🛡️ SentinelAI</div>
            <div class="sub">Autonomous Incident Intelligence Platform</div>
        </div>
        """, unsafe_allow_html=True)

    time.sleep(1.5)
    splash.empty()