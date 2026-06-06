class RiskScorer:

    @staticmethod
    def calculate(volume_score: int, anomaly_score: int):

        # weighted fusion model
        score = (volume_score * 0.6) + (anomaly_score * 0.4)

        return min(int(score), 100)

    @staticmethod
    def severity(score: int):

        if score >= 85:
            return "CRITICAL"

        if score >= 70:
            return "HIGH"

        if score >= 50:
            return "MEDIUM"

        return "LOW"