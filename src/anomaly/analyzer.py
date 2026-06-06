from src.anomaly.detectors import StatisticalDetector, MLDetector
from src.anomaly.scorer import RiskScorer
from src.anomaly.classifier import AttackClassifier
from src.anomaly.models import ThreatEvent


class AnomalyAnalyzer:

    def __init__(self):
        self.ml = MLDetector()

    def analyze_series(self, source: str, values: list):

        if not values or len(values) < 2:
            return None

        # STATISTICAL
        stat_flag, stat_score = StatisticalDetector.detect_spike(values)

        # ML
        ml_flag, ml_score = self.ml.detect(values)

        # RISK SCORE
        score = RiskScorer.calculate(stat_score, ml_score)
        severity = RiskScorer.severity(score)

        # NO ANOMALY FILTER
        if not stat_flag and not ml_flag:
            return None

        return ThreatEvent(
            source=source,
            anomaly_type="VOLUME_SPIKE",
            severity=severity,
            score=score,
            attack_type=AttackClassifier.classify(values),
            description=f"Anomaly detected in {source}",
            recommendation="Investigate logs and correlate with authentication/network activity",
            record_count=values[-1]
        )