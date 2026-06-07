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

        # 1. STATISTICAL ENGINE DETECTS SPIKES (Z-SCORE)
        stat_flag, stat_score = StatisticalDetector.detect_spike(values)

        # 2. MACHINE LEARNING ENGINE RUNS PATTERN CHECK (ISOLATION FOREST)
        ml_flag, ml_score = self.ml.detect(values)

        # 3. FUSION RISK SCORE AND SEVERITY ASSIGNMENT
        score = RiskScorer.calculate(stat_score, ml_score)
        severity = RiskScorer.severity(score)

        # 4. FILTER OUT NORMAL LOG TRAFFIC WINDOWS
        if not stat_flag and not ml_flag:
            return None

        # 5. CONSTRUCT CORRECTLY MAPPED PYDANTIC THREAT OBJECT
        return ThreatEvent(
            source=source,
            anomaly_type="VOLUME_SPIKE",
            severity=severity,
            score=score,
            attack_type=AttackClassifier.classify(values),
            description=f"Automated anomaly detected in {source} log stream.",
            recommendation="Investigate raw logs via Splunk queries and correlate source IP profiles.",
            data_points=int(values[-1])  # FIXED: Perfectly maps to data_points schema parameter
        )
