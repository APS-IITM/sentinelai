import random
import uuid
from datetime import datetime
from typing import List, Dict, Any


class AttackScenarios:

    @staticmethod
    def brute_force() -> List[Dict[str, Any]]:
        events = []
        targets = ["/api/v1/auth/login", "/admin/wp-login.php", "/ssh/v2"]
        for _ in range(random.randint(15, 45)):
            events.append({
                "message": "Failed password attempts exceeded metrics thresholds",
                "target_endpoint": random.choice(targets),
                "attempt_ip": f"{random.randint(1,254)}.{random.randint(1,254)}.23.11",
                "user_agent": "Mozilla/5.0 (Hydra Bruteforcer Suite/9.5)"
            })
        return events

    @staticmethod
    def port_scan() -> List[Dict[str, Any]]:
        events = []
        ports = [22, 23, 80, 443, 8080, 3306, 5432]
        for p in ports:
            events.append({
                "message": "TCP SYN probe alert on block configuration scanning profile",
                "targeted_port": p,
                "scan_type": "SYN-Sweep-Nmap"
            })
        return events

    @staticmethod
    def ddos() -> List[Dict[str, Any]]:
        return [{
            "message": "Ingress bandwidth saturation threshold breached on Layer 7 infrastructure",
            "pps_count": random.randint(120000, 500000),
            "drop_percentage": random.uniform(12.5, 48.2)
        } for _ in range(random.randint(50, 100))]

    @staticmethod
    def error_storm() -> List[Dict[str, Any]]:
        services = ["auth-worker", "payment-gateway", "db-pool-router"]
        return [{
            "message": "Fatal: Unhandled exceptions cascading operational service crash-loops",
            "subsystem": random.choice(services),
            "stack_trace": "NullReferenceException at core.internal.allocator.invoke()"
        } for _ in range(random.randint(10, 25))]

    @staticmethod
    def wrap(events: List[Dict[str, Any]], attack_type: str, source: str) -> List[Dict[str, Any]]:
        severity_levels = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        wrapped = []

        for e in events:
            severity = random.choices(
                severity_levels,
                weights=[0.4, 0.3, 0.2, 0.1]
            )[0]

            wrapped.append({
                "event_id": str(uuid.uuid4()),
                "timestamp": datetime.utcnow().isoformat(),
                "source": source,
                "attack_type": attack_type,
                "severity": severity,
                "event": e
            })

        return wrapped