class MitreMapper:

    MAPPING = {

        "BRUTE_FORCE_ATTACK": [
            "T1110 - Brute Force"
        ],

        "NETWORK_SCAN": [
            "T1046 - Network Service Discovery"
        ],

        "DDOS_ATTACK": [
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
            attack_type,
            ["Unknown Technique"]
        )

    @classmethod
    def map_events(cls, events):

        techniques = set()

        for event in events:

            attack = getattr(
                event,
                "attack_type",
                "UNKNOWN"
            )

            techniques.update(
                cls.map_attack(attack)
            )

        return sorted(list(techniques))