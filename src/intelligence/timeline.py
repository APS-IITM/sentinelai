from datetime import datetime


class TimelineBuilder:

    @staticmethod
    def build(events):

        timeline = []

        for event in events:

            ts = getattr(event, "timestamp", None)

            if not ts:
                ts = datetime.now()

            timeline.append({
                "event_id": getattr(event, "event_id", "N/A"),
                "time": ts.isoformat(),
                "source": getattr(event, "source", "UNKNOWN_SRC"),
                "attack": getattr(event, "attack_type", "UNKNOWN_ATTACK"),
                "severity": getattr(event, "severity", "LOW"),
                "score": getattr(event, "score", 0)
            })

        timeline.sort(
            key=lambda x: x["time"]
        )

        return timeline