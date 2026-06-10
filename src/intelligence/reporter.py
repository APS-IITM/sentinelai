class StoryGenerator:

    @staticmethod
    def _get_val(obj, key, default=None):
        if isinstance(obj, dict):
            return obj.get(key, default)
        return getattr(obj, key, default)

    @staticmethod
    def generate(events, incident_type):
        # FIXED: Use safe dictionary parsing for narrative generation loops
        sources = {
            str(StoryGenerator._get_val(e, "source", "UNKNOWN"))
            for e in events
        }

        attacks = [
            str(StoryGenerator._get_val(e, "attack_type", "UNKNOWN"))
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