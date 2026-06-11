class AttackRunner:

    def __init__(self):
        self.file = "attack_stream.log"

    def push(self, events, attack_type):

        if not events:
            return

        with open(self.file, "a") as f:
            for e in events:
                try:
                    f.write(str(e) + "\n")
                except Exception:
                    continue