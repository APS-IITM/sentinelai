from datetime import datetime


class AttackRunner:

    def __init__(self):
        self.file = "attack_stream.log"

    def push(self, events, attack_type):

        with open(self.file, "a") as f:

            for e in events:

                f.write(e.model_dump_json() + "\n")