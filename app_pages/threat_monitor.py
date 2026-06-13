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

# ================================================================
# TABLE — click a row to instantly trigger AI analysis
# ================================================================
st.markdown("### 📋 Threat Table — click any row to analyze")

event = st.dataframe(
    df,
    use_container_width=True,
    on_select="rerun",          # rerun immediately on row click
    selection_mode="single-row",
    hide_index=True,
)

selected_rows = event.selection.rows

# ================================================================
# AI REPORT — auto-generates the moment a row is selected
# ================================================================
if selected_rows:
    row = df.iloc[selected_rows[0]].to_dict()

    st.markdown("---")
    st.markdown(f"### 🎯 AI Report — `{row.get('attack_type', 'Unknown')}` · `{row.get('severity', '?')}` severity")

    class Wrap:
        def __init__(self, r):
            self.source      = r.get("source")
            self.attack_type = r.get("attack_type")
            self.severity    = r.get("severity")
            self.description = r.get("description", "")
            self.data_points = r.get("data_points", 0)

    with st.spinner("Generating AI report..."):
        result = main.generate_ai_report(Wrap(row))

    st.markdown(result)
else:
    st.info("👆 Click any row above to instantly generate an AI threat report.")