import streamlit as st
import pandas as pd
from app_pages.ui.supabase_loader import get_anomalies

st.title("🔍 Threat Monitor Feed")
st.caption("Active monitoring engine syncing straight from Supabase logs")
st.markdown("---")

data = get_anomalies()

if not data:
    st.warning("Telemetry stream empty. No threats recorded in remote database.")
    st.stop()

df = pd.DataFrame(data)

st.markdown("<div class='card'>", unsafe_allow_html=True)
st.dataframe(df, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)