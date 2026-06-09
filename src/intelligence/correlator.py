class EventCorrelator:

    @staticmethod
    def _get_attr(e, key, default=None):
        """
        Safe getter for both dict and object inputs.
        """
        if isinstance(e, dict):
            return e.get(key, default)
        return getattr(e, key, default)

    @staticmethod
    def correlate(events):

        if not events:
            return "UNKNOWN", 0

        attacks = set()

        for e in events:
            attack_type = EventCorrelator._get_attr(e, "attack_type", "UNKNOWN")
            attacks.add(attack_type)

        # Normalize
        attacks.discard(None)
        attacks.discard("UNKNOWN")

        if not attacks:
            return "UNKNOWN", 0

        # =========================
        # RULE ENGINE (CORRELATION)
        # =========================

        if "BRUTE_FORCE_ATTACK" in attacks and "NETWORK_SCAN" in attacks:
            return "RECON_TO_CREDENTIAL_ATTACK", 90

        if "NETWORK_SCAN" in attacks and "DDOS_ATTACK" in attacks:
            return "RECON_TO_DDOS", 85

        if "BRUTE_FORCE_ATTACK" in attacks and "SYSTEM_EXPLOIT" in attacks:
            return "EXPLOITATION_CHAIN_ATTACK", 88

        if len(attacks) > 1:
            return "MULTI_STAGE_ATTACK", 75

        return list(attacks)[0], 60