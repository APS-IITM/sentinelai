import time
import subprocess
import threading
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class DataChangeHandler(FileSystemEventHandler):

    def __init__(self, repo_path: str, buffer):
        self.repo_path = Path(repo_path)
        self.buffer = buffer

    def on_modified(self, event):

        if event.is_directory:
            return

        if not event.src_path.endswith(".json"):
            return

        print(f"[DATA-SYNC] Detected change: {event.src_path}")

        # Instead of committing immediately → buffer it
        self.buffer["dirty"] = True
        self.buffer["last_change"] = time.time()


class DataSyncManager:

    def __init__(self, repo_path: str, interval_minutes=3):
        self.repo_path = Path(repo_path)
        self.interval = interval_minutes * 60

        self.buffer = {
            "dirty": False,
            "last_change": 0
        }

        self.observer = Observer()
        self.stop_flag = False

    # =========================
    # GIT OPERATION (SAFE)
    # =========================
    def commit_and_push(self):

        try:
            subprocess.run(["git", "add", "data/"], cwd=self.repo_path, check=True)

            msg = f"auto-sync: data update @ {time.strftime('%Y-%m-%d %H:%M:%S')}"

            subprocess.run(
                ["git", "commit", "-m", msg],
                cwd=self.repo_path,
                check=True
            )

            subprocess.run(["git", "push"], cwd=self.repo_path, check=True)

            print("[DATA-SYNC] ✅ Commit successful")

        except subprocess.CalledProcessError as e:
            print(f"[DATA-SYNC] ⚠️ Git skipped: {e}")

    # =========================
    # BACKGROUND LOOP
    # =========================
    def _worker(self):

        while not self.stop_flag:

            time.sleep(self.interval)

            if self.buffer["dirty"]:

                print("[DATA-SYNC] ⏳ Processing buffered changes...")

                self.commit_and_push()

                self.buffer["dirty"] = False

            else:
                print("[DATA-SYNC] No changes detected in interval")

    # =========================
    # START SYSTEM
    # =========================
    def start(self):

        handler = DataChangeHandler(str(self.repo_path), self.buffer)

        self.observer.schedule(
            handler,
            path=str(self.repo_path / "data"),
            recursive=True
        )

        self.observer.start()

        print("[DATA-SYNC] 🚀 Watching started (batch mode enabled)")

        thread = threading.Thread(target=self._worker, daemon=True)
        thread.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("[DATA-SYNC] Stopping...")
            self.stop_flag = True
            self.observer.stop()

        self.observer.join()