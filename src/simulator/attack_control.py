from typing import Dict, Any
from src.simulator.engine import AttackEngine
from src.simulator.state import AttackState


class AttackControlSystem:

    def __init__(self):
        self.engine = AttackEngine()

    def launch(self, attack_type: str) -> Dict[str, Any]:
        return self.engine.launch_attack(attack_type)

    def status(self) -> Dict[str, Any]:
        return AttackState.get_state()

    def stop(self, attack_id: str) -> Dict[str, Any]:
        AttackState.stop(attack_id)
        return {
            "attack_id": attack_id,
            "status": "stopped"
        }