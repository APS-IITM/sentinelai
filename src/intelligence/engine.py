from src.intelligence.models import IntelligenceReport
from src.intelligence.correlator import EventCorrelator
from src.intelligence.timeline import TimelineBuilder
from src.intelligence.mitre import MitreMapper
from src.intelligence.reporter import StoryGenerator
from src.storage.intelligence_store import IntelligenceStore


class IntelligenceEngine:

    SEVERITY_WEIGHTS = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
        "CRITICAL": 4
    }

    @staticmethod
    def _get_val(obj, key, default=None):
        """Helper to safely extract keys regardless of whether inputs are dicts or objects."""
        if isinstance(obj, dict):
            return obj.get(key, default)
        return getattr(obj, key, default)

    def analyze(self, events):
        if not events:
            return None

        incident_type, confidence = EventCorrelator.correlate(events)

        # FIXED: Safeguarded extraction logic to accept both db dict rows and model objects safely
        severity = max(
            (str(self._get_val(e, "severity", "LOW")) for e in events),
            key=lambda x: self.SEVERITY_WEIGHTS.get(x.upper(), 0),
            default="LOW"
        )

        timeline = TimelineBuilder.build(events)
        mitre = []

        for event in events:
            # FIXED: Safe retrieval for mapping
            attack_type = self._get_val(event, "attack_type", "UNKNOWN")
            mitre.extend(
                MitreMapper.map_attack(attack_type)
            )

        story = StoryGenerator.generate(events, incident_type)

        report = IntelligenceReport(
            incident_type=incident_type,
            severity=severity,
            attack_story=story,
            timeline=timeline,
            mitre_techniques=list(set(mitre)),
            recommendations=[
                "Review affected systems",
                "Validate suspicious accounts",
                "Investigate source IPs",
                "Increase monitoring",
                "Review firewall rules"
            ],
            event_count=len(events)
        )

        IntelligenceStore.save(
            report.model_dump(mode="json")
        )

        return report