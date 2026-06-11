
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
            logger.warning(
                f"⚠️ Skipping stream {source}: "
                f"Insufficient data points "
                f"({len(values) if values else 0}/10)."
            )
            return None

        # ---------------------------------------------------------
        # STEP 1: DETECTION LAYER
        # ---------------------------------------------------------

        stat_flag, stat_score = StatisticalDetector.detect_spike(values)
        ml_flag, ml_score = self.ml.detect(values)

        score = RiskScorer.calculate(stat_score, ml_score)
        severity = RiskScorer.severity(score)

        if not stat_flag and not ml_flag:
            logger.debug(f"No anomaly detected for {source}")
            return None

        threat = ThreatEvent(
            source=source,
            anomaly_type="VOLUME_SPIKE",
            severity=severity,
            score=score,
            attack_type=AttackClassifier.classify(values),
            description=f"Automated anomaly detected in {source} log stream.",
            recommendations=[
                "Investigate raw logs via Splunk queries and correlate source IP profiles."
            ],
            data_points=int(values[-1]),
        )

        logger.info(
            f"🚨 Anomaly Detected | "
            f"Source={source} | "
            f"Severity={severity} | "
            f"Score={score:.2f}"
        )

        # ---------------------------------------------------------
        # STEP 2: STORE ANOMALY
        # ---------------------------------------------------------

        try:

            AnomalyStore.save(
                threat.model_dump(mode="json")
            )

            logger.success(
                f"✅ Successfully committed anomaly "
                f"for {source} to AnomalyStore."
            )

        except Exception:

            logger.exception(
                "❌ Failed writing anomaly to AnomalyStore"
            )

            try:
                st.error(
                    "Database Write Failure [AnomalyStore]"
                )
            except Exception:
                pass

        # ---------------------------------------------------------
        # STEP 3: INTELLIGENCE PIPELINE
        # ---------------------------------------------------------

        threat_payload = [threat]

        logger.debug(
            f"⚡ Sending ThreatEvent to IntelligenceEngine | "
            f"Source={threat.source} | "
            f"Severity={threat.severity} | "
            f"Attack={threat.attack_type}"
        )

        logger.debug(
            f"Payload Type: {type(threat_payload[0])}"
        )

        try:

            reports = self.intel_engine.analyze(
                threat_payload
            )

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

                try:
                    st.toast(
                        f"🛡️ Generated {len(reports)} intelligence report(s)"
                    )
                except Exception:
                    pass

            else:

                logger.warning(
                    "⚠️ IntelligenceEngine returned no reports."
                )

        except Exception as e:

            logger.exception(
                "❌ CRITICAL CRASH inside IntelligenceEngine"
            )

            try:

                with st.expander(
                    "🚨 Intelligence Pipeline Debugger",
                    expanded=True
                ):

                    st.error(str(e))

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

                    st.markdown("### Payload Type")

                    st.code(
                        str(type(threat_payload[0]))
                    )

                    st.markdown("### Payload Content")

                    st.json(
                        threat.model_dump(
                            mode="json"
                        )
                    )

            except Exception:
                pass

        return threat

