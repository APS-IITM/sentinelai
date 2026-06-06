from src.anomaly.detector import (
    StatisticalDetector,
    MLDetector
)

from src.anomaly.scorer import RiskScorer
from src.anomaly.models import ThreatFinding


class AnomalyAnalyzer:

    def __init__(self):

        self.ml_detector = MLDetector()

    def analyze_series(
        self,
        source,
        values
    ):

        stat_anomaly = (
            StatisticalDetector
            .z_score_detection(values)
        )

        ml_anomaly = (
            self.ml_detector
            .detect(values)
        )

        count = values[-1]

        score = (
            RiskScorer
            .score_from_volume(count)
        )

        severity = (
            RiskScorer
            .severity(score)
        )

        if not stat_anomaly and not ml_anomaly:
            return None

        return ThreatFinding(
            source=source,
            severity=severity,
            score=score,
            anomaly_type="Volume Spike",
            description=(
                f"Abnormal activity detected "
                f"in {source}"
            ),
            recommendation=(
                "Investigate source logs "
                "for malicious behavior"
            ),
            record_count=count
        )