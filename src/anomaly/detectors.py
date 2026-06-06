import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from scipy.stats import zscore


class StatisticalDetector:

    @staticmethod
    def detect_spike(values):

        if len(values) < 5:
            return False, 0

        series = pd.Series(values)

        z_scores = zscore(series)

        latest_z = abs(z_scores[-1])

        return latest_z > 2.5, latest_z * 20


class MLDetector:

    def __init__(self):

        self.model = IsolationForest(
            contamination=0.05,
            random_state=42
        )

    def detect(self, values):

        if len(values) < 10:
            return False, 0

        data = np.array(values).reshape(-1, 1)

        self.model.fit(data)

        prediction = self.model.predict(data)

        # -1 = anomaly
        is_anomaly = prediction[-1] == -1

        anomaly_score = (
            80 if is_anomaly else 10
        )

        return is_anomaly, anomaly_score