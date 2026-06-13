import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from scipy.stats import zscore
from loguru import logger

class StatisticalDetector:

    @staticmethod
    def detect_spike(values):
        if len(values) < 5:
            return False, 0

        series = pd.Series(values, dtype=float)

        if series.std() == 0:
            return False, 0

        z_scores = zscore(series)
        latest_z = abs(z_scores[-1])

        if np.isnan(latest_z):
            return False, 0

        # ✅ Lowered from 2.5 → 1.8 for simulated attack volumes
        # 2.5 requires an extreme outlier; 1.8 catches realistic spikes
        threshold = 1.8
        return bool(latest_z > threshold), float(latest_z * 20)


class MLDetector:

    def __init__(self):
        # ✅ Raised contamination: your data IS mostly attacks, not 5% anomalies
        self.model = IsolationForest(
            contamination=0.15,  # was 0.05 — too strict for simulated attack streams
            random_state=42
        )

    def detect(self, values):
        if len(values) < 10:
            return False, 0

        data = np.array(values, dtype=float).reshape(-1, 1)

        # ✅ Guard: if all values identical, ML can't learn anything
        if np.std(data) == 0:
            return False, 0

        try:
            self.model.fit(data[:-1])
            prediction = self.model.predict(data[-1:])
            score = self.model.decision_function(data[-1:])

            is_anomaly = bool(prediction[0] == -1)
            # ✅ Use actual decision score instead of hardcoded 80/10
            anomaly_score = float(np.clip(-score[0] * 100, 0, 100))
            return is_anomaly, anomaly_score

        except Exception as e:
            logger.warning(f"MLDetector failed: {e}")
            return False, 0