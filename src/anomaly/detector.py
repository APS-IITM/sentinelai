import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest


class StatisticalDetector:

    @staticmethod
    def z_score_detection(values):

        if len(values) < 5:
            return False

        series = pd.Series(values)

        mean = series.mean()
        std = series.std()

        if std == 0:
            return False

        latest = series.iloc[-1]

        z_score = (latest - mean) / std

        return abs(z_score) > 2.5


class MLDetector:

    def __init__(self):

        self.model = IsolationForest(
            contamination=0.05,
            random_state=42
        )

    def detect(self, values):

        if len(values) < 10:
            return False

        data = np.array(values).reshape(-1, 1)

        predictions = self.model.fit_predict(data)

        return predictions[-1] == -1