class EventCorrelator:

    @staticmethod
    def correlate(events):

        if not events:
            return None

        attacks = {
            e.attack_type
            for e in events
        }

        if (
            "BRUTE_FORCE_ATTACK" in attacks
            and "NETWORK_SCAN" in attacks
        ):
            return "RECON_TO_CREDENTIAL_ATTACK"

        if (
            "NETWORK_SCAN" in attacks
            and "DDOS_ATTACK" in attacks
        ):
            return "RECON_TO_DDOS"

        if len(attacks) > 1:
            return "MULTI_STAGE_ATTACK"

        return list(attacks)[0]