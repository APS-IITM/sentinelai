from datetime import datetime, timezone


class TimelineBuilder:

    @staticmethod
    def build(events):

        timeline = []

        for event in events:

            is_dict = isinstance(event, dict)

            ts = (
                event.get("timestamp")
                if is_dict
                else getattr(event, "timestamp", None)
            )

            if not ts:

                ts = datetime.now(
                    timezone.utc
                )

            if isinstance(ts, datetime):

                ts = ts.isoformat()

            timeline.append({

                "event_id": (
                    event.get("event_id", "N/A")
                    if is_dict
                    else getattr(
                        event,
                        "event_id",
                        "N/A"
                    )
                ),

                "time": ts,

                "source": (
                    event.get(
                        "source",
                        "UNKNOWN_SRC"
                    )
                    if is_dict
                    else getattr(
                        event,
                        "source",
                        "UNKNOWN_SRC"
                    )
                ),

                "attack": (
                    event.get(
                        "attack_type",
                        "UNKNOWN_ATTACK"
                    )
                    if is_dict
                    else getattr(
                        event,
                        "attack_type",
                        "UNKNOWN_ATTACK"
                    )
                ),

                "severity": (
                    event.get(
                        "severity",
                        "LOW"
                    )
                    if is_dict
                    else getattr(
                        event,
                        "severity",
                        "LOW"
                    )
                ),

                "score": (
                    event.get(
                        "score",
                        0
                    )
                    if is_dict
                    else getattr(
                        event,
                        "score",
                        0
                    )
                )
            })

        timeline.sort(
            key=lambda x: x["time"]
        )

        return timeline