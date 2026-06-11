import uuid
import random
from typing import Dict, Any
from src.simulator.state import AttackState
from src.simulator.controller import AttackSimulator


class AttackEngine:

    def __init__(self):
        self.simulator = AttackSimulator()

    def launch_attack(self, attack_type: str) -> Dict[str, Any]:
        attack_id = str(uuid.uuid4())[:8]

        # 🎯 AUTOMATIC RANDOM SEVERITY ALLOCATION
        # Distributes the threats realistically so you get a rich variance of test metrics
        severity_options = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
        selected_severity = random.choices(
            severity_options, 
            weights=[0.35, 0.35, 0.20, 0.10] # 10% chance for a severe production emergency
        )[0]

        # 1. Pipeline generation executes structural raw logs according to chosen context
        events = self.simulator.run_attack(attack_type, severity=selected_severity)

        # 2. Log deployment and state synchronization sequence
        AttackState.start_attack(attack_id, attack_type, selected_severity)
        AttackState.update(attack_id, len(events))
        AttackState.complete(attack_id)

        return {
            "attack_id": attack_id,
            "attack_type": attack_type,
            "events": len(events),
            "severity": selected_severity,
            "status": "COMPLETED",
        }