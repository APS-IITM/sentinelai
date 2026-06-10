import uuid

from src.simulator.state import AttackState
from src.simulator.controller import AttackSimulator

from app_pages.ui_components.supabase_loader import save_intel_report


class AttackEngine:

    def __init__(self):
        self.simulator = AttackSimulator()
        

    def launch_attack(self, attack_type):
        attack_id = str(uuid.uuid4())[:8]

        AttackState.start_attack(attack_id, attack_type)

        # GENERATE EVENTS
        events = self.simulator.run_attack(attack_type)

        AttackState.update(attack_id, len(events))
        AttackState.complete(attack_id)

        

        

        return {
            "attack_id": attack_id,
            "attack_type": attack_type,
            "events": len(events),
            "status": "COMPLETED",
        }