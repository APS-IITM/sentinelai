import streamlit as st
import pandas as pd
from src.storage.anomaly_store import AnomalyStore

st.title("🔍 Threat Monitor Feed")

data = AnomalyStore.get_all()

if not data:
    st.warning("No stored threat data.")
    st.stop()

df = pd.DataFrame(data)

st.dataframe(df, use_container_width=True)