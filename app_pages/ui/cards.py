import streamlit as st

def metric_card(title, value, delta=None):
    st.markdown(f"""
    <div class="card">
        <h4>{title}</h4>
        <h2>{value}</h2>
        <small>{delta if delta else ""}</small>
    </div>
    """, unsafe_allow_html=True)