import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.title("✨ Executive Dashboard")
st.caption("Real-time system security posture and event analytics.")

# Top Metrics Row
m1, m2, m3, m4 = st.columns(4)
m1.metric(label="Total Logs Scanned", value="1,245,892", delta="+12% today")
m2.metric(label="Threats Detected", value="142", delta="18 active", delta_color="inverse")
m3.metric(label="Critical Alerts", value="3", delta="Action Required", delta_color="off")
m4.metric(label="Affected Systems", value="12 Host Assets", delta="-2 resolved")

st.markdown("---")

# Visualizations Row
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("Log Volume vs. Threat Trend")
    # Generating mock time-series data
    df_trend = pd.DataFrame({
        'Time': pd.date_range(start='2026-06-08 00:00', periods=24, freq='H'),
        'Log Volume (k)': np.random.randint(40, 60, size=24),
        'Threats': np.random.randint(0, 8, size=24)
    })
    fig = px.line(df_trend, x='Time', y=['Log Volume (k)', 'Threats'], 
                  color_discrete_sequence=["#C0C0C0", "#D4AF37"], template="plotly_white")
    fig.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=300)
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Severity Distribution")
    df_pie = pd.DataFrame({
        "Severity": ["Critical", "High", "Medium", "Low"],
        "Count": [3, 24, 45, 70]
    })
    fig_pie = px.pie(df_pie, values='Count', names='Severity', 
                     color_discrete_sequence=["#8B0000", "#D4AF37", "#E6C280", "#F5F5F5"], template="plotly_white")
    fig_pie.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=300, showlegend=False)
    st.plotly_chart(fig_pie, use_container_width=True)

# Recent Urgent Incidents Table
st.subheader("Immediate Attention Required")
mock_data = {
    "Incident ID": ["INC-2026-8841", "INC-2026-8842", "INC-2026-8843"],
    "Timestamp": ["2026-06-08 15:42", "2026-06-08 14:10", "2026-06-08 11:02"],
    "Attack Target": ["Production-DB-01", "User-JSmith-Laptop", "Auth-Gateway"],
    "Severity": ["Critical", "High", "Medium"]
}
st.dataframe(pd.DataFrame(mock_data), use_container_width=True, hide_index=True)