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
        


        threat_payload = [threat]

        logger.debug(
            f"⚡ Sending ThreatEvent to IntelligenceEngine | "
            f"Source={threat.source} | "
            f"Severity={threat.severity} | "
            f"Attack={threat.attack_type}"
        )

        try:

            reports = self.intel_engine.analyze(threat_payload)

            if reports:

                logger.success(
                    f"✅ IntelligenceEngine generated "
                    f"{len(reports)} report(s)"
                )

                for report in reports:

                    logger.info(
                        f"📄 CTI Report | "
                        f"ID={report.report_id} | "
                        f"Type={report.incident_type} | "
                        f"Severity={report.severity}"
                    )

                if st.runtime.exists():
                    st.toast(
                        f"🛡️ Intelligence Engine generated "
                        f"{len(reports)} report(s)",
                        icon="🛡️"
                    )

            else:

                logger.warning(
                    "⚠️ IntelligenceEngine returned no reports."
                )

        except Exception as e:

            logger.exception(
                "❌ CRITICAL CRASH inside IntelligenceEngine processing loop!"
            )

            if st.runtime.exists():

                with st.expander(
                    "🚨 PIPELINE CRASH: Intelligence Engine Debugger",
                    expanded=True
                ):

                    st.error(f"Error: {str(e)}")

                    st.markdown("### Diagnostics")

                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(
                            "Source",
                            source
                        )

                        st.metric(
                            "Severity",
                            severity
                        )

                    with col2:
                        st.metric(
                            "Score",
                            f"{score:.2f}"
                        )

                        st.metric(
                            "Payload Size",
                            len(threat_payload)
                        )

                    st.markdown("### Payload")

                    if hasattr(threat, "model_dump"):
                        st.json(threat.model_dump(mode="json"))
                    else:
                        st.write(threat)    
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