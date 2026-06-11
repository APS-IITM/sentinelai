import random
import uuid
from datetime import datetime


class AttackScenarios:

    @staticmethod
    def _wrap(events, attack_type, source):

        wrapped = []

        severity_levels = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]

        for e in events:

            severity = random.choices(
                severity_levels,
                weights=[0.4, 0.3, 0.2, 0.1]
            )[0]

            wrapped.append({
                "id": str(uuid.uuid4()),
                "timestamp": datetime.utcnow().isoformat(),
                "attack_type": attack_type,
                "source": source,
                "severity": severity,
                "payload": e
            })

        return wrapped