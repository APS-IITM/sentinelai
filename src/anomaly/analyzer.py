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
            recommendations=["Investigate raw logs via Splunk queries and correlate source IP profiles."],
            data_points=int(values[-1])
        )

        # 1. Save raw anomaly to the database
        AnomalyStore.save(
            threat.model_dump(mode="json")
        )

        # ⛓️ 2. THE PIPELINE LINK: Automatically hand off the threat event to the CTI engine!
        # Wrapping it in a list container ensures your engine's iterator loop can process it instantly.
        try:
            self.intel_engine.analyze([threat])
        except Exception as e:
            # Prevent an analytical CTI breakdown from crashing your main logging service
            print(f"⚠️ Intelligence Engine cascade failed: {str(e)}")

        return threat