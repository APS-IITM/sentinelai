import streamlit as st
from loguru import logger

from src.anomaly.detectors import StatisticalDetector, MLDetector
from src.anomaly.scorer import RiskScorer
from src.anomaly.classifier import AttackClassifier
from src.anomaly.models import ThreatEvent
from src.storage.anomaly_store import AnomalyStore


class AnomalyAnalyzer:

    def __init__(self):
        self.ml = MLDetector()

    def analyze_series(self, source: str, values: list):

        if not values or len(values) < 10:
            logger.warning(
                f"⚠️ Skipping stream {source}: insufficient data"
            )
            return None

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
            description=f"Anomaly detected in {source}",
            recommendations=[
                "Investigate logs and correlate IP patterns"
            ],
            data_points=int(values[-1])
        )

        logger.info(
            f"🚨 Anomaly | Source={source} | Severity={severity}"
        )

        try:
            AnomalyStore.save(threat.model_dump(mode="json"))
        except Exception as e:
            logger.error(f"DB error: {e}")
            st.error("Anomaly storage failure")

        return threat