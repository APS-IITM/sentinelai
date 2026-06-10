class AttackState:

    active_attacks = {}

    @classmethod
    def start_attack(cls, attack_id, attack_type):

        cls.active_attacks[attack_id] = {
            "type": attack_type,
            "status": "RUNNING",
            "events_generated": 0
        }

    @classmethod
    def update(cls, attack_id, count):

        if attack_id in cls.active_attacks:
            cls.active_attacks[attack_id]["events_generated"] += count

    @classmethod
    def stop(cls, attack_id):

        if attack_id in cls.active_attacks:
            cls.active_attacks[attack_id]["status"] = "STOPPED"

    @classmethod
    def complete(cls, attack_id):

        if attack_id in cls.active_attacks:
            cls.active_attacks[attack_id]["status"] = "COMPLETED"

    @classmethod
    def get_state(cls):

        return cls.active_attacks