import streamlit as st
import pandas as pd
import main

st.title("🔍 Tactical Threat Monitor")
st.markdown("---")

data = main.get_all_anomalies()

if not data:
    st.warning("No data")
    st.stop()

df = pd.DataFrame(data)

st.dataframe(df, use_container_width=True)

st.markdown("### 🎯 Single Event Analysis")

if "id" in df.columns:
    selected = st.selectbox("Select ID", df["id"].tolist())

    if st.button("Analyze"):
        row = df[df["id"] == selected].iloc[0].to_dict()

        class Wrap:
            def __init__(self, r):
                self.source = r.get("source")
                self.attack_type = r.get("attack_type")
                self.severity = r.get("severity")
                self.description = r.get("description", "")
                self.data_points = r.get("data_points", 0)

        result = main.generate_ai_report(Wrap(row))

        st.markdown(result)