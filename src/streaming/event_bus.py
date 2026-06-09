import time
from collections import deque


class EventBus:

    _events = deque(maxlen=200)

    @classmethod
    def publish(cls, event: dict):

        event["timestamp"] = time.time()
        cls._events.append(event)

    @classmethod
    def get_latest(cls, limit=20):

        return list(cls._events)[-limit:]

    @classmethod
    def clear(cls):

        cls._events.clear()