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
        
        # 🎯 FIX: Changed z_scores.iloc[-1] to z_scores[-1] because zscore() returns a NumPy Array!
        latest_z = abs(z_scores[-1]) 

        if np.isnan(latest_z):
            return False, 0

        # Returns True if Z-Score exceeds threshold (2.5), and maps out a score multiplier
        return bool(latest_z > 2.5), float(latest_z * 20)


class MLDetector:

    def __init__(self):
        self.model = IsolationForest(
            contamination=0.05,
            random_state=42
        )

    def detect(self, values):
        if len(values) < 10:
            return False, 0

        # If data is completely flat prior to the anomaly, inject micro-noise 
        # to prevent singular dimensional covariance tracking issues in sklearn
        raw_data = np.array(values, dtype=float)
        if np.std(raw_data[:-1]) == 0:
            # Add negligible noise to variance calculation baseline
            raw_data[:-1] += np.random.normal(0, 0.01, size=len(raw_data)-1)

        data = raw_data.reshape(-1, 1)

        try:
            self.model.fit(data[:-1])
            prediction = self.model.predict(data[-1:])
            
            is_anomaly = bool(prediction[0] == -1)
            anomaly_score = 80.0 if is_anomaly else 10.0
            return is_anomaly, anomaly_score
            
        except Exception:
            return False, 0