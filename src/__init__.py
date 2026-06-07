"""sentinelai package

Lightweight package initializer. Exposes package version and a small
utility function for quick checks.
"""

__all__ = ["__version__", "ping"]

__version__ = "0.0.1"

def ping() -> str:
    """Return a simple readiness string.

    Useful for quick health checks: import sentinelai; sentinelai.ping()
    """
    return "sentinelai: OK"
