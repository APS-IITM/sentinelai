from datetime import datetime, timezone
from loguru import logger

class EventCorrelator:

    @staticmethod
    def _get_attr(e, key, default=None):
        """Safe getter for both dict and object inputs."""
        if isinstance(e, dict):
            return e.get(key, default)
        return getattr(e, key, default)

    @staticmethod
    def correlate(events):
        if not events:
            return "UNKNOWN", 0

        attacks = set()
        for e in events:
            attack_type = EventCorrelator._get_attr(e, "attack_type", "UNKNOWN")
            attacks.add(attack_type)

        attacks.discard(None)
        attacks.discard("UNKNOWN")

        if not attacks:
            return "UNKNOWN", 0

        # =========================================================
        # RULE ENGINE (CORRELATION) - Harmonized with Classifier keys
        # =========================================================
        if "BRUTE_FORCE" in attacks and "PORT_SCAN" in attacks:
            return "RECON_TO_CREDENTIAL_ATTACK", 90

        if "PORT_SCAN" in attacks and "DOS_ATTACK" in attacks:
            return "RECON_TO_DDOS", 85

        if "BRUTE_FORCE" in attacks and "SYSTEM_EXPLOIT" in attacks:
            return "EXPLOITATION_CHAIN_ATTACK", 88

        if len(attacks) > 1:
            return "MULTI_STAGE_ATTACK", 75

        return list(attacks)[0], 60


class MitreMapper:

    # ✅ Harmonized directly with your AttackClassifier outputs to fix tracking errors
    MAPPING = {
        "BRUTE_FORCE": ["T1110 - Brute Force"],
        "PORT_SCAN": ["T1046 - Network Service Discovery"],
        "DOS_ATTACK": ["T1498 - Network Denial of Service"],
        "ERROR_STORM": ["T1499 - Endpoint Denial of Service"],
        "RECON_TO_CREDENTIAL_ATTACK": [
            "T1046 - Network Service Discovery",
            "T1110 - Brute Force"
        ],
        "RECON_TO_DDOS": [
            "T1046 - Network Service Discovery",
            "T1498 - Network Denial of Service"
        ],
        "MULTI_STAGE_ATTACK": [
            "T1046 - Network Service Discovery",
            "T1110 - Brute Force",
            "T1498 - Network Denial of Service"
        ]
    }

    @classmethod
    def map_attack(cls, attack_type):
        return cls.MAPPING.get(attack_type, ["Unknown Technique"])

    @classmethod
    def map_events(cls, events):
        techniques = set()
        for event in events:
            # ✅ Fixed type leak bug using the robust dict-safe check
            if isinstance(event, dict):
                attack = event.get("attack_type", "UNKNOWN")
            else:
                attack = getattr(event, "attack_type", "UNKNOWN")
                
            techniques.update(cls.map_attack(attack))
        return sorted(list(techniques))


class TimelineBuilder:

    @staticmethod
    def build(events):
        timeline = []

        for event in events:
            # ✅ Fixed: Use a robust check to pull variables from serialized JSON payloads safely
            is_dict = isinstance(event, dict)
            
            ts = event.get("timestamp") if is_dict else getattr(event, "timestamp", None)
            
            # Reconstruct string timestamps back into clean tracking elements safely
            if not ts:
                ts = datetime.now(timezone.utc).isoformat()
            elif isinstance(ts, datetime):
                ts = ts.isoformat()

            timeline.append({
                "event_id": event.get("event_id", "N/A") if is_dict else getattr(event, "event_id", "N/A"),
                "time": ts,
                "source": event.get("source", "UNKNOWN_SRC") if is_dict else getattr(event, "source", "UNKNOWN_SRC"),
                "attack": event.get("attack_type", "UNKNOWN_ATTACK") if is_dict else getattr(event, "attack_type", "UNKNOWN_ATTACK"),
                "severity": event.get("severity", "LOW") if is_dict else getattr(event, "severity", "LOW"),
                "score": event.get("score", 0) if is_dict else getattr(event, "score", 0)
            })

        timeline.sort(key=lambda x: x["time"])
        return timeline