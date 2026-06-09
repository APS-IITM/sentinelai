import time
import subprocess
import threading
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class DataChangeHandler(FileSystemEventHandler):

    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.last_commit_time = 0
        self.cooldown = 5  # seconds (prevents spam commits)

    # Triggered on any file modification
    def on_modified(self, event):
        if event.is_directory:
            return

        if not event.src_path.endswith(".json"):
            return

        now = time.time()

        # debounce
        if now - self.last_commit_time < self.cooldown:
            return

        self.last_commit_time = now

        print(f"[DATA-SYNC] Change detected: {event.src_path}")
        self.commit_and_push()


    def commit_and_push(self):

        try:
            # STEP 1: stage only data folder
            subprocess.run(
                ["git", "add", "data/"],
                cwd=self.repo_path,
                check=True
            )

            # STEP 2: commit
            msg = f"auto-sync: update data store @ {time.strftime('%Y-%m-%d %H:%M:%S')}"
            subprocess.run(
                ["git", "commit", "-m", msg],
                cwd=self.repo_path,
                check=True
            )

            # STEP 3: push
            subprocess.run(
                ["git", "push"],
                cwd=self.repo_path,
                check=True
            )

            print("[DATA-SYNC] ✅ Auto commit + push successful")

        except subprocess.CalledProcessError as e:
            print(f"[DATA-SYNC] ⚠️ Git operation skipped: {e}")


class DataSyncManager:

    def __init__(self, repo_path: str):
        self.repo_path = repo_path
        self.observer = Observer()

    def start(self):
        event_handler = DataChangeHandler(self.repo_path)

        self.observer.schedule(
            event_handler,
            path=str(Path(self.repo_path) / "data"),
            recursive=True
        )

        self.observer.start()

        print("[DATA-SYNC] 🚀 Watching data/ folder for changes...")

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("[DATA-SYNC] Stopping watcher...")
            self.observer.stop()

        self.observer.join()


# ======================================================
# RUN AS STANDALONE SERVICE
# ======================================================
if __name__ == "__main__":
    import os

    repo_root = os.getcwd()

    manager = DataSyncManager(repo_root)
    manager.start()