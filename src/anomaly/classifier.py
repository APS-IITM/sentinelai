class AttackClassifier:

    @staticmethod
    def classify(values):

        if len(values) == 0:
            return "UNKNOWN"

        avg = sum(values) / len(values)
        peak = max(values)

        if peak > avg * 3:
            return "BRUTE_FORCE_ATTACK"

        if peak > avg * 2:
            return "NETWORK_SCAN"

        if avg > 100:
            return "ERROR_STORM"

        return "NORMAL_ACTIVITY"