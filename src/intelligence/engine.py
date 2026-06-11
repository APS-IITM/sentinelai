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

        "RECON_TO_CREDENTIAL_ATTACK": [
            "Block reconnaissance sources immediately.",
            "Enable MFA enforcement.",
            "Review authentication telemetry."
        ],

        "RECON_TO_DDOS": [
            "Activate DDoS protection controls.",
            "Review firewall telemetry.",
            "Rate-limit suspicious traffic sources."
        ],

        "MULTI_STAGE_ATTACK": [
            "Escalate to SOC analysts immediately.",
            "Review full attack chain telemetry.",
            "Contain affected systems."
        ],

        "DEFAULT": [
            "Isolate highly affected target infrastructure systems from local subnets.",
            "Audit access logs across surrounding directories for lateral movement signatures.",
            "Perform comprehensive full-stack security telemetry scans immediately."
        ]
    }

    @staticmethod
    def _get_val(obj, key, default=None):

        if isinstance(obj, dict):
            return obj.get(key, default)

        return getattr(obj, key, default)

    def analyze(self, events):

        logger.info("🧠 IntelligenceEngine Execution Started")

        if not events:

            logger.warning(
                "⚠️ IntelligenceEngine received empty event list."
            )

            return []

        logger.info(
            f"📥 Received {len(events)} event(s)"
        )

        logger.info(
            f"📦 Event Type: {type(events[0])}"
        )

        reports_generated = []

        try:

            unique_severities = {

                str(
                    self._get_val(
                        event,
                        "severity",
                        "LOW"
                    )
                ).upper()

                for event in events
            }

            logger.info(
                f"🎯 Severity Groups Detected: {list(unique_severities)}"
            )

        except Exception:

            logger.exception(
                "❌ Failed calculating severity groups."
            )

            return []

        for target_severity in unique_severities:

            logger.info(
                f"🔍 Processing Severity Group: {target_severity}"
            )

            severity_events = [

                event

                for event in events

                if str(
                    self._get_val(
                        event,
                        "severity",
                        "LOW"
                    )
                ).upper() == target_severity
            ]

            if not severity_events:

                logger.warning(
                    f"⚠️ No events found for {target_severity}"
                )

                continue

            try:

                logger.info(
                    f"⚡ Correlating {len(severity_events)} event(s)"
                )

                incident_type, confidence = (
                    EventCorrelator.correlate(
                        severity_events
                    )
                )

                logger.success(
                    f"Correlation Result: "
                    f"{incident_type} "
                    f"({confidence}% confidence)"
                )

            except Exception:

                logger.exception(
                    "❌ EventCorrelator failed."
                )

                continue

            try:

                logger.info(
                    "🕒 Building timeline..."
                )

                timeline = TimelineBuilder.build(
                    severity_events
                )

                logger.success(
                    f"Timeline Built ({len(timeline)} entries)"
                )

            except Exception:

                logger.exception(
                    "❌ TimelineBuilder failed."
                )

                continue

            try:

                logger.info(
                    "🎯 Mapping MITRE ATT&CK techniques..."
                )

                mitre = []

                for event in severity_events:

                    attack_type = self._get_val(
                        event,
                        "attack_type",
                        "UNKNOWN"
                    )

                    mitre.extend(
                        MitreMapper.map_attack(
                            attack_type
                        )
                    )

                mitre = sorted(
                    list(set(mitre))
                )

                logger.success(
                    f"MITRE Techniques: {mitre}"
                )

            except Exception:

                logger.exception(
                    "❌ MITRE Mapping failed."
                )

                mitre = []

            try:

                logger.info(
                    "📖 Generating attack narrative..."
                )

                story = StoryGenerator.generate(
                    severity_events,
                    incident_type
                )

            except Exception:

                logger.exception(
                    "❌ Story generation failed."
                )

                story = (
                    "Automated incident narrative "
                    "generation failed."
                )

            dynamic_recommendations = (
                self.RECOMMENDATION_PLAYBOOKS.get(
                    incident_type,
                    self.RECOMMENDATION_PLAYBOOKS["DEFAULT"]
                )
            )

            try:

                report = IntelligenceReport(
                    incident_type=incident_type,
                    severity=target_severity,
                    attack_story=story,
                    timeline=timeline,
                    mitre_techniques=mitre,
                    recommendations=dynamic_recommendations,
                    event_count=len(severity_events)
                )

                logger.success(
                    f"📄 Generated Report "
                    f"{report.report_id}"
                )

            except Exception:

                logger.exception(
                    "❌ IntelligenceReport construction failed."
                )

                continue

            try:

                logger.info(
                    f"💾 Saving Report "
                    f"{report.report_id}"
                )

                IntelligenceStore.save(
                    report.model_dump(
                        mode="json"
                    )
                )

                logger.success(
                    f"✅ Saved Report "
                    f"{report.report_id}"
                )

            except Exception:

                logger.exception(
                    "❌ Failed to save IntelligenceReport."
                )

            reports_generated.append(
                report
            )

        logger.success(
            f"🏁 IntelligenceEngine completed. "
            f"Generated {len(reports_generated)} report(s)."
        )

        return reports_generated