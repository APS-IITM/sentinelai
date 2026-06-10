import streamlit as st
from loguru import logger  

from src.anomaly.detectors import StatisticalDetector, MLDetector
from src.anomaly.scorer import RiskScorer
from src.anomaly.classifier import AttackClassifier
from src.anomaly.models import ThreatEvent
from src.storage.anomaly_store import AnomalyStore
from src.intelligence.engine import IntelligenceEngine

class AnomalyAnalyzer:

    def __init__(self):
        self.ml = MLDetector()
        self.intel_engine = IntelligenceEngine()

    def analyze_series(self, source: str, values: list):
        
        if not values or len(values) < 10:
            logger.warning(f"⚠️ Skipping stream {source}: Insufficient data points ({len(values) if values else 0}/10).")
            return None

        # ---------------------------------------------------------
        # 🕵️ STEP 1: DETECTION LAYER
        # ---------------------------------------------------------
        stat_flag, stat_score = StatisticalDetector.detect_spike(values)
        ml_flag, ml_score = self.ml.detect(values)

        score = RiskScorer.calculate(stat_score, ml_score)
        severity = RiskScorer.severity(score)

        if not stat_flag and not ml_flag:
            return None

        # Build Data Payload
        threat = ThreatEvent(
            source=source,
            anomaly_type="VOLUME_SPIKE",
            severity=severity,
            score=score,
            attack_type=AttackClassifier.classify(values),
            description=f"Automated anomaly detected in {source} log stream.",
            recommendations=["Investigate raw logs via Splunk queries and correlate source IP profiles."],
            data_points=int(values[-1])
        )

        logger.info(f"🚨 Anomaly Detected | Source: {source} | Severity: {severity} | Score: {score}")

        # ---------------------------------------------------------
        # 💾 STEP 2: PERSISTENCE LAYER
        # ---------------------------------------------------------
        try:
            AnomalyStore.save(threat.model_dump(mode="json"))
            logger.success(f"Successfully committed anomaly for {source} to AnomalyStore.")
        except Exception as db_err:
            logger.error(f"❌ Failed writing to AnomalyStore: {str(db_err)}")
            st.error(f"Database Write Failure [AnomalyStore]: {str(db_err)}")

        # ---------------------------------------------------------
        # ⛓️ STEP 3: PIPELINE DEBBUGGER LINK (INTELLIGENCE ENGINE)
        # ---------------------------------------------------------
        threat_payload = [threat.model_dump(mode="json")] if hasattr(threat, "model_dump") else [threat]

        logger.debug(f"⚡ Cascading anomaly payload to IntelligenceEngine: {threat_payload}")

        try:
            # Execute CTI analysis
            report = self.intel_engine.analyze(threat_payload)
            
            if report:
                logger.success(f"✅ IntelligenceEngine successfully generated CTI Report ID: {getattr(report, 'report_id', 'N/A')}")
                # Optional: Render runtime updates on the Streamlit dashboard if live
                if st.runtime.exists():
                    st.toast(f"ℹ️ CTI Engine Compiled {severity} Threat Report!", icon="🛡️")
            else:
                logger.warning("⚠️ IntelligenceEngine completed execution but returned an empty report.")
                
        except Exception as e:
            # Capture full trace details in your terminal/cloud logs
            logger.exception("❌ CRITICAL CRASH inside IntelligenceEngine processing loop!")
            
            # Surface an interactive visual debugger window directly inside your Streamlit App
            if st.runtime.exists():
                with st.expander("🚨 PIPELINE CRASH: Intelligence Engine Debugger", expanded=True):
                    st.error(f"**Error:** {str(e)}")
                    st.markdown("### Contextual Diagnostics")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(label="Target Source", value=source)
                        st.metric(label="Calculated Severity", value=str(severity))
                    with col2:
                        st.metric(label="Calculated Score", value=f"{score:.2f}")
                        st.metric(label="Payload Size Sent", value=f"{len(threat_payload)} item(s)")
                    
                    st.markdown("#### Exact Payload Sent to Engine:")
                    st.json(threat_payload)

        return threat