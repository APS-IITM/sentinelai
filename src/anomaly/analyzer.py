from src.anomaly.detectors import StatisticalDetector, MLDetector
from src.anomaly.scorer import RiskScorer
from src.anomaly.classifier import AttackClassifier
from src.anomaly.models import ThreatEvent
from src.storage.anomaly_store import AnomalyStore


class AnomalyAnalyzer:

    def __init__(self):
        self.ml = MLDetector()

    def analyze_series(self, source: str, values: list):
        # FIXED: Enforce a minimum window length of 10 elements 
        # This gives both your Z-Score and Isolation Forest enough data points to compute baseline calculations
        if not values or len(values) < 10:
            return None

        stat_flag, stat_score = StatisticalDetector.detect_spike(values)
        ml_flag, ml_score = self.ml.detect(values)

        score = RiskScorer.calculate(stat_score, ml_score)
        severity = RiskScorer.severity(score)

        if not stat_flag and not ml_flag:
            return None

        threat = ThreatEvent(
            source=source,
            anomaly_type="VOLUME_SPIKE",
            severity=severity,
            score=score,
            attack_type=AttackClassifier.classify(values),
            description=f"Automated anomaly detected in {source} log stream.",
            recommendation="Investigate raw logs via Splunk queries and correlate source IP profiles.",
            data_points=int(values[-1])
        )

        # Persist anomaly
        AnomalyStore.save(
            threat.model_dump(mode="json")
        )

        return threat