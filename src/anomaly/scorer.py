class RiskScorer: 
    @staticmethod
    def score_from_volume(count:int):
        if count > 1000:
            return 95
        elif count > 500:
            return 80
        elif count > 200:
            return 65
        elif count > 100:
            return 50
        else:
            return 20
    def severity(score:int):
        if score > 90:
            return "Critical"
        elif score > 70:
            return "High"
        elif score > 50:
            return "Medium"
        else:
            return "Low"