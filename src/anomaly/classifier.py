import numpy as np

class AttackClassifier:

    @staticmethod
    def classify(values: list) -> str:
        """
        Evaluates trend step changes over arrays to classify the anomaly signature.
        """
        if not values or len(values) < 3:
            return "UNKNOWN_TRAFFIC"

        arr = np.array(values, dtype=float)
        diffs = np.diff(arr)

        # Pattern A: Sudden massive volumetric jump
        if diffs[-1] > np.median(arr) * 5:
            return "BRUTE_FORCE"

        # Pattern B: Sequential increases over successive frames (Reconnaissance footprint)
        if len(diffs) >= 3 and all(x > 0 for x in diffs[-3:]):
            return "PORT_SCAN"

        # Pattern C: Persistent high saturation exceeding the initial baseline
        if arr[-1] > np.mean(arr[:-3]) * 3:
            return "DOS_ATTACK"

        return "VOLUME_SPIKE"