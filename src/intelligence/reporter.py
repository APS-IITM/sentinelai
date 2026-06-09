class StoryGenerator:

    @staticmethod
    def generate(
        events,
        incident_type
    ):

        sources = {
            e.source
            for e in events
        }

        attacks = [
            e.attack_type
            for e in events
        ]

        return (
            f"SentinelAI correlated "
            f"{len(events)} events "
            f"across "
            f"{len(sources)} monitored sources. "
            f"The activity pattern matches "
            f"{incident_type}. "
            f"Observed attack stages include "
            f"{', '.join(set(attacks))}. "
            f"Investigation is recommended."
        )