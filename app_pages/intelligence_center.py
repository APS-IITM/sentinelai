import streamlit as st
import pandas as pd
from datetime import datetime
import main

st.title("🧭 Intelligence Center")
st.markdown("---")

raw = main.get_all_intelligence_reports()

if not raw:
    st.info("No data")
    st.stop()

df = pd.DataFrame(raw)

if "created_at" in df.columns:
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

st.subheader("Filters")

filtered = df.copy()

st.dataframe(filtered, use_container_width=True)

st.markdown("---")

page_size = 5
page = st.number_input("Page", 1, 100, 1)

start = (page - 1) * page_size
end = start + page_size

for _, r in filtered.iloc[start:end].iterrows():
    st.markdown(f"""
    <div class="card">
        <h4>{r.get('incident_type')}</h4>
        <p>{r.get('severity')}</p>
        <p>{r.get('attack_story')}</p>
    </div>
    """, unsafe_allow_html=True)