import random


class AttackScenarios:

    @staticmethod
    def _wrap(events):

        severity_levels = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

        for e in events:

            e["severity"] = random.choices(
                severity_levels,
                weights=[0.4, 0.3, 0.2, 0.1]
            )[0]

        return events


    @staticmethod
    def brute_force():

        events = [
            {
                "event": "login_failed",
                "user": "admin",
                "ip": "192.168.1.10"
            }
            for _ in range(random.randint(20, 60))
        ]

        return AttackScenarios._wrap(events)


    @staticmethod
    def port_scan():

        events = [
            {
                "event": "connection_attempt",
                "ip": "10.0.0.5",
                "port": port
            }
            for port in range(20, 100)
        ]

        return AttackScenarios._wrap(events)


    @staticmethod
    def ddos():

        events = [
            {
                "event": "request",
                "ip": f"10.0.0.{random.randint(1,255)}",
                "size": random.randint(100,1000)
            }
            for _ in range(200)
        ]

        return AttackScenarios._wrap(events)


    @staticmethod
    def error_storm():

        events = [
            {
                "event": "error",
                "service": "auth",
                "code": 500
            }
            for _ in range(100)
        ]

        return AttackScenarios._wrap(events)