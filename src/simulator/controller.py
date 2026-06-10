from src.simulator.scenarios import AttackScenarios
from src.simulator.runner import AttackRunner


class AttackSimulator:

    def __init__(self):
        self.runner = AttackRunner()

    def run_attack(self, attack_type):
        # FIXED: Added string normalization step to prevent route drops
        normalized_type = str(attack_type).lower().strip()

        if normalized_type in ["brute_force", "brute_force_attack"]:
            events = AttackScenarios.brute_force()

        elif normalized_type in ["port_scan", "network_scan"]:
            events = AttackScenarios.port_scan()

        elif normalized_type in ["ddos", "ddos_attack"]:
            events = AttackScenarios.ddos()

        elif normalized_type in ["error_storm"]:
            events = AttackScenarios.error_storm()

        else:
            events = []

        # log stream
        if events:
            self.runner.push(events, attack_type)

        return events