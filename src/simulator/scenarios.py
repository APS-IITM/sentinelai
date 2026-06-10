import random
import uuid
from datetime import datetime
from src.core.event_schema import SOCEvent


class AttackScenarios:

    @staticmethod
    def _wrap(events, attack_type, source):
        severity_levels = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        wrapped = []

        # Scoring weights to pass down realistic metrics
        score_map = {"LOW": 20, "MEDIUM": 55, "HIGH": 75, "CRITICAL": 95}

        for e in events:
            severity = random.choices(
                severity_levels,
                weights=[0.4, 0.3, 0.2, 0.1]
            )[0]

            # FIXED: Enriched model generation to protect Intelligence metrics
            wrapped.append(
                SOCEvent(
                    event_id=str(uuid.uuid4()),
                    source=source,
                    attack_type=attack_type,
                    severity=severity,
                    score=score_map[severity] + random.randint(-5, 5),
                    description=f"Simulated {attack_type} event activity targeted at {source}.",
                    raw_event=e,
                    timestamp=datetime.utcnow()
                )
            )

        return wrapped

    @staticmethod
    def brute_force():
        events = [
            {"event": "login_failed", "user": "admin", "ip": "192.168.1.10"}
            for _ in range(random.randint(20, 60))
        ]
        return AttackScenarios._wrap(events, "BRUTE_FORCE_ATTACK", "AUTH")

    @staticmethod
    def port_scan():
        events = [
            {"event": "connection_attempt", "ip": "10.0.0.5", "port": p}
            for p in range(20, 100)
        ]
        return AttackScenarios._wrap(events, "NETWORK_SCAN", "NETWORK")

    @staticmethod
    def ddos():
        events = [
            {"event": "request", "ip": f"10.0.0.{random.randint(1,255)}", "size": random.randint(100,1000)}
            for _ in range(200)
        ]
        return AttackScenarios._wrap(events, "DDOS_ATTACK", "NETWORK")

    @staticmethod
    def error_storm():
        events = [
            {"event": "error", "service": "auth", "code": 500}
            for _ in range(100)
        ]
        return AttackScenarios._wrap(events, "ERROR_STORM", "SYSTEM")