class StoryGenerator:

    @staticmethod
    def generate(events, incident_type):

        attack_names = [
            e.attack_type
            for e in events
        ]

        return (
            f"SentinelAI detected "
            f"{incident_type}. "
            f"Observed attack stages: "
            f"{', '.join(attack_names)}."
        )