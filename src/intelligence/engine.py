from loguru import logger
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

    # 🛡️ DYNAMIC MITIGATION REMEDIATION PLAYBOOKS
    RECOMMENDATION_PLAYBOOKS = {
        "PORT_SCAN": [
            "Deploy progressive firewall drop rules against the source IP network block.",
            "Disable unnecessary exposed listener ports on edge infrastructure.",
            "Verify network access control lists (ACLs) follow a zero-trust policy."
        ],
        "BRUTE_FORCE": [
            "Temporarily lock out target corporate user accounts experiencing systemic failures.",
            "Enforce immediate Multi-Factor Authentication (MFA) challenges across active sessions.",
            "Correlate geolocational signatures of incoming traffic streams."
        ],
        "DOS_ATTACK": [
            "Engage upstream cloud scrubbing centers or CDN rate-limiting rule profiles.",
            "Enable aggressive TCP intercept and SYN-cookie protections on edge devices.",
            "Isolate non-essential public-facing application endpoint nodes."
        ],
        "DEFAULT": [
            "Isolate highly affected target infrastructure systems from local subnets.",
            "Audit access logs across surrounding directories for lateral movement signatures.",
            "Perform comprehensive full-stack security telemetry scans immediately."
        ]
    }

    @staticmethod
    def _get_val(obj, key, default=None):
        """Helper to safely extract keys regardless of whether inputs are dicts or objects."""
        if isinstance(obj, dict):
            return obj.get(key, default)
        return getattr(obj, key, default)

    def analyze(self, events):
        if not events:
            logger.warning("⚠️ IntelligenceEngine received an empty events matrix. Processing aborted.")
            return []

        reports_generated = []
        
        # Unify incoming event severities to compute group iterations accurately
        unique_severities = set(str(self._get_val(e, "severity", "LOW")).upper() for e in events)

        for target_severity in unique_severities:
            
            severity_events = [
                e for e in events 
                if str(self._get_val(e, "severity", "LOW")).upper() == target_severity
            ]
            
            if not severity_events:
                continue

            # Run correlator engines to deduce threat vector patterns
            incident_type, confidence = EventCorrelator.correlate(severity_events)
            timeline = TimelineBuilder.build(severity_events)
            
            mitre = []
            for event in severity_events:
                attack_type = self._get_val(event, "attack_type", "UNKNOWN")
                mitre.extend(MitreMapper.map_attack(attack_type))

            story = StoryGenerator.generate(severity_events, incident_type)

            # 🧠 DYNAMIC REMEDIATION ROUTING
            # Extract recommendations based on the classified incident context
            dynamic_recommendations = self.RECOMMENDATION_PLAYBOOKS.get(
                incident_type, 
                self.RECOMMENDATION_PLAYBOOKS["DEFAULT"]
            )

            # Instantiating the clean, structural CTI Report data object
            report = IntelligenceReport(
                incident_type=incident_type,
                severity=target_severity,
                attack_story=story,
                timeline=timeline,
                mitre_techniques=list(set(mitre)),
                recommendations=dynamic_recommendations, # ✅ Now dynamically populated
                event_count=len(severity_events)
            )

            # Commit the compiled tier threat summary down to your Database Store
            try:
                IntelligenceStore.save(report.model_dump(mode="json"))
                logger.success(f"💾 Saved {target_severity} CTI Report targeting {incident_type} to database layer.")
            except Exception as store_err:
                logger.error(f"❌ Failed to persist IntelligenceReport: {str(store_err)}")

            reports_generated.append(report)

        # ✅ FIX: Return ALL compiled tier incident tracking documents, not just index [0]
        return reports_generated