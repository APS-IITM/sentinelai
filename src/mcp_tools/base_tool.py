from src.splunk.client import connect, run_search
from src.utils.formatter import normalize_response


class BaseTool:

    def __init__(self):
        self.service = connect()

    def execute(self, query: str):
        raw = run_search(self.service, query)
        return normalize_response(raw)