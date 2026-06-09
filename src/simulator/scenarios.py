import random


class AttackScenarios:

    @staticmethod
    def brute_force():

        return [
            {
                "event": "login_failed",
                "user": "admin",
                "ip": "192.168.1.10"
            }
            for _ in range(random.randint(20, 60))
        ]

    @staticmethod
    def port_scan():

        return [
            {
                "event": "connection_attempt",
                "ip": "10.0.0.5",
                "port": port
            }
            for port in range(20, 100)
        ]

    @staticmethod
    def ddos():

        return [
            {
                "event": "request",
                "ip": f"10.0.0.{random.randint(1,255)}",
                "size": random.randint(100,1000)
            }
            for _ in range(200)
        ]

    @staticmethod
    def error_storm():

        return [
            {
                "event": "error",
                "service": "auth",
                "code": 500
            }
            for _ in range(100)
        ]