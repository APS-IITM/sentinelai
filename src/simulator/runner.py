import os
import json
import threading
from typing import List, Dict, Any


class AttackRunner:

    def __init__(self, filename: str = "attack_stream.log"):
        self.file_path = filename
        self._io_lock = threading.Lock()

    def push(self, events: List[Dict[str, Any]], attack_type: str) -> None:
        if not events:
            return

        # Ensure parent execution paths exist in runtime environment
        parent_dir = os.path.dirname(os.path.abspath(self.file_path))
        if parent_dir and not os.path.exists(parent_dir):
            os.makedirs(parent_dir, exist_ok=True)

        # Thread-locked, safe stream writing allocation
        with self._io_lock:
            try:
                with open(self.file_path, "a", encoding="utf-8") as f:
                    for e in events:
                        f.write(json.dumps(e) + "\n")
            except (IOError, OSError) as io_err:
                print(f"[FATAL WRITER EXCEPTION] Pipeline writing error: {str(io_err)}")