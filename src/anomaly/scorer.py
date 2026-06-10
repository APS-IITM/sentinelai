class RiskScorer:

    @staticmethod
    def calculate(stat_score: float, ml_score: float) -> float:
        """
        Weights and clamps incoming detector data safely.
        Balances volatile spikes with behavioral ML trends.
        """
        # Distribute weights evenly (Max 50 points per detector)
        weighted_stat = min(stat_score, 50.0)
        weighted_ml = min(ml_score, 50.0)
        
        return float(weighted_stat + weighted_ml)

    @staticmethod
    def severity(score: float) -> str:
        """Standardized qualitative tiering for corporate incident routing."""
        if score < 30:
            return "LOW"
        elif score < 60:
            return "MEDIUM"
        elif score < 85:
            return "HIGH"
        return "CRITICAL"