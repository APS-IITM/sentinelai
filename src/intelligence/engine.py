from src.intelligence.models import (
    IntelligenceReport
)

from src.intelligence.correlator import (
    EventCorrelator
)

from src.intelligence.timeline import (
    TimelineBuilder
)

from src.intelligence.mitre import (
    MitreMapper
)

from src.intelligence.reporter import (
    StoryGenerator
)

from src.storage.intelligence_store import (
    IntelligenceStore
)


class IntelligenceEngine:

    SEVERITY_WEIGHTS = {
        "LOW": 1,
        "MEDIUM": 2,
        "HIGH": 3,
        "CRITICAL": 4
    }

    def analyze(
        self,
        events
    ):

        if not events:
            return None

        incident_type, confidence = (
            EventCorrelator.correlate(events)
        )

        severity = max(
            (
                e.severity
                for e in events
            ),
            key=lambda x:
            self.SEVERITY_WEIGHTS.get(
                x.upper(),
                0
            ),
            default="LOW"
        )

        timeline = (
            TimelineBuilder.build(events)
        )

        mitre = []

        for event in events:

            mitre.extend(
                MitreMapper.map_attack(
                    event.attack_type
                )
            )

        story = (
            StoryGenerator.generate(
                events,
                incident_type
            )
        )

        report = IntelligenceReport(
            incident_type=incident_type,
            severity=severity,
            attack_story=story,
            timeline=timeline,
            mitre_techniques=list(
                set(mitre)
            ),
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
            report.model_dump(
                mode="json"
            )
        )

        return report