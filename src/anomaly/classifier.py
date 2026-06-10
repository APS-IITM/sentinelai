class AttackClassifier:

    @staticmethod
    def classify(values):
        if len(values) == 0:
            return "UNKNOWN"

        avg = sum(values) / len(values)
        peak = max(values)

        # FIXED: Evaluate absolute volume spikes first to lock down high-impact storms
        if avg > 100 and peak < (avg * 2):
            return "ERROR_STORM"

        if peak > avg * 3:
            return "BRUTE_FORCE_ATTACK"

        if peak > avg * 2:
            return "NETWORK_SCAN"

        return "NORMAL_ACTIVITY"