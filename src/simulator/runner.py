import json
from datetime import datetime


class AttackRunner:

    def __init__(self):

        self.file = "attack_stream.log"

    def push(self, events, attack_type):

        with open(self.file, "a") as f:

            for e in events:

                e["attack_type"] = attack_type
                e["timestamp"] = str(datetime.now())

                f.write(json.dumps(e) + "\n")