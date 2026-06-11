from loguru import logger

from src.intelligence.models import IntelligenceReport
from src.intelligence.correlator import EventCorrelator
from src.intelligence.timeline import TimelineBuilder
from src.intelligence.mitre import MitreMapper
from src.intelligence.reporter import StoryGenerator
from src.storage.intelligence_store import IntelligenceStore


class IntelligenceEngine:

    def _get(self, obj, key, default=None):
        if isinstance(obj, dict):
            return obj.get(key, default)
        return getattr(obj, key, default)

    def analyze(self, events):

        logger.info("🧠 Intelligence Engine Started")

        if not events:
            return []

        reports = []

        severities = {
            str(self._get(e, "severity", "LOW")).upper()
            for e in events
        }

        for severity in severities:

            group = [
                e for e in events
                if str(self._get(e, "severity", "LOW")).upper() == severity
            ]

            if not group:
                continue

            incident_type, confidence = EventCorrelator.correlate(group)

            timeline = TimelineBuilder.build(group)

            mitre = []
            for e in group:
                mitre.extend(
                    MitreMapper.map_attack(
                        self._get(e, "attack_type", "UNKNOWN")
                    )
                )

            mitre = sorted(set(mitre))

            story = StoryGenerator.generate(group, incident_type)

            report = IntelligenceReport(
                incident_type=incident_type,
                severity=severity,
                attack_story=story,
                timeline=timeline,
                mitre_techniques=mitre,
                recommendations=[],
                event_count=len(group)
            )

            IntelligenceStore.save(report.model_dump(mode="json"))

            reports.append(report)

        return reports