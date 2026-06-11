from typing import List, Dict, Any
from src.simulator.scenarios import AttackScenarios
from src.simulator.runner import AttackRunner


class AttackSimulator:

    def __init__(self):
        self.runner = AttackRunner()

    def run_attack(self, attack_type: str, severity: str) -> List[Dict[str, Any]]:
        normalized_type = str(attack_type).lower().strip()
        raw_events = []

        if normalized_type in ["brute_force", "brute_force_attack"]:
            raw_events = AttackScenarios.brute_force(severity)
        elif normalized_type in ["port_scan", "network_scan"]:
            raw_events = AttackScenarios.port_scan(severity)
        elif normalized_type in ["ddos", "ddos_attack"]:
            raw_events = AttackScenarios.ddos(severity)
        elif normalized_type in ["error_storm"]:
            raw_events = AttackScenarios.error_storm(severity)

        if not raw_events:
            return []

        # Wrap using the target overarching severity assignment
        wrapped_events = AttackScenarios.wrap(raw_events, normalized_type, source="SOC_SIM", severity=severity)

        # Offload safely up to Supabase Cloud Storage
        self.runner.push(wrapped_events, normalized_type)

        return wrapped_events