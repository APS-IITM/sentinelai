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
        
        
        if series.std() == 0:
            return False, 0

        z_scores = zscore(series)
        latest_z = abs(z_scores[-1])

        # Safely capture any unexpected NaN issues
        if np.isnan(latest_z):
            return False, 0

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

        try:
            
            self.model.fit(data)
            prediction = self.model.predict(data)
            is_anomaly = prediction[-1] == -1
            anomaly_score = 80 if is_anomaly else 10
            return is_anomaly, anomaly_score
        except Exception:
            return False, 0