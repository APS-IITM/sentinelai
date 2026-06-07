from datetime import datetime

class TimelineBuilder:
    @staticmethod
    def build(events):
        timeline = []

        for event in events:
            # Safe attribute check with a datetime fallback object
            ts = getattr(event, "timestamp", None)
            if not ts:
                ts = datetime.now()

            timeline.append({
                "time": ts.isoformat() if hasattr(ts, "isoformat") else str(ts),
                "source": getattr(event, "source", "UNKNOWN_SRC"),
                "attack": getattr(event, "attack_type", "UNKNOWN_ATTACK"),
                "severity": getattr(event, "severity", "LOW")
            })

        return timeline
