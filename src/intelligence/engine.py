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


class IntelligenceEngine:

    def analyze(self, events):

        if not events:
            return None

        incident_type = (
            EventCorrelator.correlate(
                events
            )
        )

        severity = max(
            (
                e.severity
                for e in events
            ),
            default="LOW"
        )

        timeline = (
            TimelineBuilder.build(
                events
            )
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

        return IntelligenceReport(
            incident_type=incident_type,
            severity=severity,
            attack_story=story,
            timeline=timeline,
            mitre_techniques=list(set(mitre)),
            recommendations=[
                "Review affected systems",
                "Validate suspicious accounts",
                "Investigate source IPs",
                "Increase monitoring"
            ]
        )