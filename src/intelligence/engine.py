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

        # =========================================================
        # 🛠️ FIX: GROUP EVENTS BY SEVERITY TO PREVENT SWALLOWING
        # =========================================================
        # This ensures low, medium, and high get their own distinct processing loops
        reports_generated = []
        
        # Find all unique severities present in this simulation dump
        unique_severities = set(str(self._get_val(e, "severity", "LOW")).upper() for e in events)

        for target_severity in unique_severities:
            # Filter events belonging ONLY to this specific severity tier
            severity_events = [
                e for e in events 
                if str(self._get_val(e, "severity", "LOW")).upper() == target_severity
            ]
            
            if not severity_events:
                continue

            # Run the correlation matrix against just this tier's events
            incident_type, confidence = EventCorrelator.correlate(severity_events)

            timeline = TimelineBuilder.build(severity_events)
            mitre = []

            for event in severity_events:
                attack_type = self._get_val(event, "attack_type", "UNKNOWN")
                mitre.extend(MitreMapper.map_attack(attack_type))

            story = StoryGenerator.generate(severity_events, incident_type)

            report = IntelligenceReport(
                incident_type=incident_type,
                severity=target_severity, # Stamped correctly (LOW, MEDIUM, HIGH, or CRITICAL)
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
                event_count=len(severity_events)
            )

            # Save the individual tier report to your Supabase layer
            IntelligenceStore.save(report.model_dump(mode="json"))
            reports_generated.append(report)

        # Return the last generated report or a list depending on your frontend needs
        return reports_generated[0] if reports_generated else None