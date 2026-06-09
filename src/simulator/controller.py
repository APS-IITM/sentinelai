from src.simulator.scenarios import AttackScenarios
from src.simulator.runner import AttackRunner


class AttackSimulator:

    def __init__(self):

        self.runner = AttackRunner()

    def run_attack(self, attack_type):

        if attack_type == "brute_force":
            events = AttackScenarios.brute_force()

        elif attack_type == "port_scan":
            events = AttackScenarios.port_scan()

        elif attack_type == "ddos":
            events = AttackScenarios.ddos()

        elif attack_type == "error_storm":
            events = AttackScenarios.error_storm()

        else:
            events = []

        self.runner.push(events, attack_type)

        return events