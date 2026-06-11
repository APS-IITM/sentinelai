class MitreMapper:

    MAPPING = {

        "BRUTE_FORCE": [
            "T1110 - Brute Force"
        ],

        "PORT_SCAN": [
            "T1046 - Network Service Discovery"
        ],

        "DOS_ATTACK": [
            "T1498 - Network Denial of Service"
        ],

        "ERROR_STORM": [
            "T1499 - Endpoint Denial of Service"
        ],

        "RECON_TO_CREDENTIAL_ATTACK": [
            "T1046 - Network Service Discovery",
            "T1110 - Brute Force"
        ],

        "RECON_TO_DDOS": [
            "T1046 - Network Service Discovery",
            "T1498 - Network Denial of Service"
        ],

        "MULTI_STAGE_ATTACK": [
            "T1046 - Network Service Discovery",
            "T1110 - Brute Force",
            "T1498 - Network Denial of Service"
        ]
    }

    @classmethod
    def map_attack(cls, attack_type):

        return cls.MAPPING.get(
            str(attack_type).upper(),
            ["Unknown Technique"]
        )

    @classmethod
    def map_events(cls, events):

        techniques = set()

        for event in events:

            if isinstance(event, dict):

                attack = event.get(
                    "attack_type",
                    "UNKNOWN"
                )

            else:

                attack = getattr(
                    event,
                    "attack_type",
                    "UNKNOWN"
                )

            techniques.update(
                cls.map_attack(attack)
            )

        return sorted(
            list(techniques)
        )