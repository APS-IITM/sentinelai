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

    def analyze_series(self, source: str, values: list, events: list = None):
        if not values or len(values) < 10:
            logger.warning(f"⚠️ Skipping stream {source}: insufficient data")
            return None

        stat_flag, stat_score = StatisticalDetector.detect_spike(values)
        ml_flag, ml_score = self.ml.detect(values)

        score = RiskScorer.calculate(stat_score, ml_score)
        
        # Fixed logic gate: Trigger if EITHER system flags a risk spike
        if not stat_flag and not ml_flag:
            logger.debug(f"No anomaly detected for {source}")
            return None

        # Extract underlying severity safely 
        severity = "HIGH"  # Default fallback
        if events:
            severity_order = {"LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}
            found_severities = []
            for e in events:
                if isinstance(e, dict):
                    # Check both flat and nested variations
                    sev = e.get("severity") or e.get("event", {}).get("severity")
                    if sev:
                        found_severities.append(str(sev).upper())
            
            if found_severities:
                severity = max(found_severities, key=lambda s: severity_order.get(s, 1))
            else:
                severity = RiskScorer.severity(score)
        else:
            severity = RiskScorer.severity(score)

        attack_type = AttackClassifier.classify(values, events=events)

        last_event = events[-1] if events else None

        threat = ThreatEvent(
            source=source,
            anomaly_type=attack_type if attack_type != "UNKNOWN_TRAFFIC" else "VOLUME_SPIKE",
            severity=severity,
            score=score,
            attack_type=attack_type,
            description=f"Automated threat classification system flagged {attack_type} vector on channel [{source}].",
            recommendations=[
                "Investigate logs and correlate IP patterns",
                "Deploy structural firewall rules if source volume remains unstable"
            ],
            data_points=int(values[-1]),
            metadata={
                "sample_event": last_event,
                "series_length": len(values),
                "stat_score": stat_score,
                "ml_score": ml_score
            }
        )

        logger.info(f"🚨 Anomaly Detected | Source={source} | Type={attack_type} | Severity={severity}")

        try:
            AnomalyStore.save(threat.model_dump(mode="json"))
        except Exception as e:
            logger.error(f"DB error writing threat log event context row: {e}")

        return threat