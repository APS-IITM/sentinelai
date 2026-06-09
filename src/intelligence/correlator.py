class EventCorrelator:

    @staticmethod
    def correlate(events):

        if not events:
            return (
                "UNKNOWN",
                0
            )

        attacks = {
            e.attack_type
            for e in events
        }

        if (
            "BRUTE_FORCE_ATTACK" in attacks
            and "NETWORK_SCAN" in attacks
        ):
            return (
                "RECON_TO_CREDENTIAL_ATTACK",
                90
            )

        if (
            "NETWORK_SCAN" in attacks
            and "DDOS_ATTACK" in attacks
        ):
            return (
                "RECON_TO_DDOS",
                85
            )

        if len(attacks) > 1:
            return (
                "MULTI_STAGE_ATTACK",
                75
            )

        return (
            list(attacks)[0],
            60
        )