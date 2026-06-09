from src.simulator.engine import AttackEngine
from src.simulator.state import AttackState


class AttackControlSystem:

    def __init__(self):

        self.engine = AttackEngine()

    def launch(self, attack_type):

        result = self.engine.launch_attack(
            attack_type
        )

        return result

    def status(self):

        return AttackState.get_state()

    def stop(self, attack_id):

        AttackState.stop(attack_id)

        return {
            "attack_id": attack_id,
            "status": "stopped"
        }