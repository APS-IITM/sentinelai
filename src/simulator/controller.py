from src.simulator.scenarios import AttackScenarios
from src.simulator.runner import AttackRunner


class AttackSimulator:

    def __init__(self):
        self.runner = AttackRunner()

    def run_attack(self, attack_type):

        mapping = {
            # AUTH
            "brute_force": AttackScenarios.brute_force,
            "credential_stuffing": AttackScenarios.credential_stuffing,

            # SECURITY
            "error_storm": AttackScenarios.error_storm,
            "privilege_abuse": AttackScenarios.privilege_abuse,

            # NETWORK
            "port_scan": AttackScenarios.port_scan,
            "ddos": AttackScenarios.ddos,
            "lateral_movement": AttackScenarios.lateral_movement,

            # SYSTEM
            "cpu_spike": AttackScenarios.cpu_spike,
            "service_crash": AttackScenarios.service_crash,
        }

        events = mapping.get(attack_type, lambda: [])()

        self.runner.push(events, attack_type)

        return events