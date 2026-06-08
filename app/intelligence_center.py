import streamlit as st

st.title("🧭 Threat Intelligence & MITRE Mapping")
st.caption("Correlated multi-stage attack story lines structured around TTP framework indicators.")

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("🛡️ Attack Progression Story")
    st.markdown("""
    1. **Reconnaissance** *External IP port scan recognized on internet gateway.*
    2. **Access Execution** *High rate failed login spikes matching brute-force profile.*
    3. **Persistence Attempt** *New local root account creation flagged.*
    4. **Impact Operations** *Data exfiltration payload signature triggered via unexpected ports.*
    """)

with col2:
    st.subheader("📊 MITRE ATT&CK Mapping matrix")
    
    # Grid UI displaying standard structural tags
    g1, g2 = st.columns(2)
    with g1:
        st.markdown("""
        **[T1046] Network Service Scanning** *Status:* Active Detection  
        *Source Matrix:* Network Discovery Systems
        """)
        st.markdown("---")
        st.markdown("""
        **[T1110] Brute Force Logins** *Status:* Correlated Match  
        *Source Matrix:* Security Event Logs
        """)
    with g2:
        st.markdown("""
        **[T1078] Valid Accounts Manipulation** *Status:* High Suspicion  
        *Source Matrix:* Host Monitoring System
        """)
        st.markdown("---")
        st.markdown("""
        **[T1020] Automated Data Exfiltration** *Status:* Flagged Alert  
        *Source Matrix:* Firewall Telemetry Data
        """)