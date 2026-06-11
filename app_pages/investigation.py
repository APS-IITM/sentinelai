import streamlit as st
import pandas as pd
import main

st.title("🧰 Investigation Console")
st.markdown("---")

tool = st.selectbox("Dataset", ["auth", "network", "system", "security"])

if st.button("Fetch"):

    mapping = {
        "auth": main.get_auth_data,
        "network": main.get_network_data,
        "system": main.get_system_data,
        "security": main.get_security_data
    }

    data = mapping[tool]()

    if data:
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No data found")