import asyncio
from datetime import datetime
from loguru import logger


class GlobalAlertStore:
    """
    Thread-safe global alert system for SentinelAI.
    Works across daemon + Streamlit dashboards.
    """

    _alerts = []
    _lock = asyncio.Lock()

    @classmethod
    async def push_alert(cls, alert: dict):
        async with cls._lock:
            alert["timestamp"] = datetime.utcnow().isoformat()
            cls._alerts.append(alert)

            # keep memory bounded
            if len(cls._alerts) > 500:
                cls._alerts = cls._alerts[-500:]

        logger.warning(f"🚨 ALERT GENERATED: {alert.get('title', 'Unknown')}")

    @classmethod
    async def get_alerts(cls, limit=50):
        async with cls._lock:
            return list(reversed(cls._alerts[-limit:]))

    @classmethod
    async def clear(cls):
        async with cls._lock:
            cls._alerts.clear()