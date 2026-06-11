import threading
from typing import Dict, Any


class AttackState:
    # Class-level dictionary protected by thread allocation locks
    _lock = threading.Lock()
    active_attacks: Dict[str, Any] = {}

    @classmethod
    def start_attack(cls, attack_id: str, attack_type: str, severity: str = "LOW"):
        with cls._lock:
            cls.active_attacks[attack_id] = {
                "type": attack_type,
                "status": "RUNNING",
                "events_generated": 0,
                "severity": severity
            }

    @classmethod
    def update(cls, attack_id: str, count: int):
        with cls._lock:
            if attack_id in cls.active_attacks:
                cls.active_attacks[attack_id]["events_generated"] += count

    @classmethod
    def stop(cls, attack_id: str):
        with cls._lock:
            if attack_id in cls.active_attacks:
                cls.active_attacks[attack_id]["status"] = "STOPPED"

    @classmethod
    def complete(cls, attack_id: str):
        with cls._lock:
            if attack_id in cls.active_attacks:
                cls.active_attacks[attack_id]["status"] = "COMPLETED"

    @classmethod
    def get_state(cls) -> Dict[str, Any]:
        with cls._lock:
            # Return copy to prevent mutability leakage during rendering iterations
            return dict(cls.active_attacks)