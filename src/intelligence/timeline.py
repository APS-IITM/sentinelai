from datetime import datetime

class TimelineBuilder:
    @staticmethod
    def build(events):
        timeline = []
        for event in events:
            timeline.append({
                "time": event.timestamp.isoformat(), 
                "source": event.source,
                "attack": event.attack_type,
                "severity": event.severity
            })
        return timeline
