import random


class AttackScenarios:

    SEVERITY = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

    # =========================
    # WRAPPER 
    # =========================
    @staticmethod
    def _wrap(events, domain):
        for e in events:
            e["severity"] = random.choices(
                AttackScenarios.SEVERITY,
                weights=[0.35, 0.30, 0.25, 0.10]
            )[0]

            e["domain"] = domain

        return events


    # =========================
    # AUTH ATTACKS
    # =========================
    @staticmethod
    def brute_force():
        events = [
            {
                "event": "login_failed",
                "user": "admin",
                "ip": f"192.168.1.{random.randint(1,255)}"
            }
            for _ in range(random.randint(30, 80))
        ]
        return AttackScenarios._wrap(events, "AUTH")


    @staticmethod
    def credential_stuffing():
        events = [
            {
                "event": "login_attempt",
                "user": f"user{random.randint(1,1000)}",
                "ip": f"10.0.0.{random.randint(1,255)}"
            }
            for _ in range(random.randint(40, 100))
        ]
        return AttackScenarios._wrap(events, "AUTH")


    # =========================
    # SECURITY ATTACKS
    # =========================
    @staticmethod
    def error_storm():
        events = [
            {
                "event": "error",
                "service": "auth",
                "code": 500
            }
            for _ in range(random.randint(50, 120))
        ]
        return AttackScenarios._wrap(events, "SECURITY")


    @staticmethod
    def privilege_abuse():
        events = [
            {
                "event": "unauthorized_access",
                "user": "root",
                "action": "escalation_attempt"
            }
            for _ in range(random.randint(20, 60))
        ]
        return AttackScenarios._wrap(events, "SECURITY")


    # =========================
    # NETWORK ATTACKS
    # =========================
    @staticmethod
    def port_scan():
        events = [
            {
                "event": "connection_attempt",
                "ip": "10.0.0.5",
                "port": port
            }
            for port in range(20, 120)
        ]
        return AttackScenarios._wrap(events, "NETWORK")


    @staticmethod
    def ddos():
        events = [
            {
                "event": "request",
                "ip": f"10.0.0.{random.randint(1,255)}",
                "size": random.randint(100,1500)
            }
            for _ in range(300)
        ]
        return AttackScenarios._wrap(events, "NETWORK")


    @staticmethod
    def lateral_movement():
        events = [
            {
                "event": "internal_access",
                "source": f"host-{random.randint(1,50)}",
                "target": f"host-{random.randint(51,100)}"
            }
            for _ in range(random.randint(20, 70))
        ]
        return AttackScenarios._wrap(events, "NETWORK")


    # =========================
    # SYSTEM ATTACKS
    # =========================
    @staticmethod
    def cpu_spike():
        events = [
            {
                "event": "cpu_spike",
                "usage": random.randint(80, 100)
            }
            for _ in range(random.randint(20, 50))
        ]
        return AttackScenarios._wrap(events, "SYSTEM")


    @staticmethod
    def service_crash():
        events = [
            {
                "event": "service_down",
                "service": "api-gateway"
            }
            for _ in range(random.randint(10, 40))
        ]
        return AttackScenarios._wrap(events, "SYSTEM")