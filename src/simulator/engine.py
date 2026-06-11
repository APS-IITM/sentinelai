import uuid
from typing import Dict, Any
from src.simulator.state import AttackState
from src.simulator.controller import AttackSimulator


class AttackEngine:

    def __init__(self):
        self.simulator = AttackSimulator()

    def launch_attack(self, attack_type: str) -> Dict[str, Any]:
        attack_id = str(uuid.uuid4())[:8]

        # 1. Pipeline generation executes structural raw logs
        events = self.simulator.run_attack(attack_type)
        
        # Calculate standard macro severity for UI metadata display from wrapped logs
        if events:
            severities = [ev.get("severity", "LOW") for ev in events]
            if "CRITICAL" in severities:
                base_sev = "CRITICAL"
            elif "HIGH" in severities:
                base_sev = "HIGH"
            elif "MEDIUM" in severities:
                base_sev = "MEDIUM"
            else:
                base_sev = "LOW"
        else:
            base_sev = "LOW"

        # 2. Log configuration deployment sequence
        AttackState.start_attack(attack_id, attack_type, base_sev)
        AttackState.update(attack_id, len(events))
        AttackState.complete(attack_id)

        return {
            "attack_id": attack_id,
            "attack_type": attack_type,
            "events": len(events),
            "severity": base_sev,
            "status": "COMPLETED",
        }