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
            "T1499 - Endpoint DoS"
        ]
    }

    @classmethod
    def map_attack(cls, attack_type):

        return cls.MAPPING.get(
            attack_type,
            ["Unknown Technique"]
        )