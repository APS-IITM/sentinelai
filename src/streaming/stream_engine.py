import threading
import time

from src.streaming.event_bus import EventBus
from src.mcp_tools.system_tools import SystemTools
from src.anomaly.analyzer import AnomalyAnalyzer


class StreamEngine:

    def __init__(self):

        self.system_tool = SystemTools()
        self.analyzer = AnomalyAnalyzer()
        self.running = False

    def start_stream(self):

        self.running = True

        thread = threading.Thread(
            target=self._stream_loop,
            daemon=True
        )

        thread.start()

    def stop_stream(self):

        self.running = False

    def _stream_loop(self):

        while self.running:

            try:

                # 1. Pull live logs
                logs = self.system_tool.get_system_logs(limit=10)

                # 2. Convert to series
                series = self._extract_series(logs)

                # 3. Run anomaly detection
                if series:

                    result = self.analyzer.analyze_series(
                        "LIVE_SYSTEM",
                        series
                    )

                    if result:

                        EventBus.publish({
                            "type": "ANOMALY",
                            "payload": result.model_dump()
                        })

                    else:

                        EventBus.publish({
                            "type": "NORMAL",
                            "payload": {"status": "ok"}
                        })

                time.sleep(3)

            except Exception as e:

                EventBus.publish({
                    "type": "ERROR",
                    "payload": str(e)
                })

                time.sleep(3)

    def _extract_series(self, logs):

        values = []

        for log in logs:

            if "count" in log:

                try:
                    values.append(int(log["count"]))
                except:
                    pass

        return values