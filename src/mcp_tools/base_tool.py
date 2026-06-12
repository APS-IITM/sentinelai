import asyncio
from loguru import logger

from src.splunk.client import connect, run_search
from src.utils.formatter import normalize_response
from src.storage.mcp_store import MCPStore


class BaseTool:
    """
    SentinelAI MCP Base Tool

    Responsibilities:
    - Manage Splunk connection (lazy singleton)
    - Execute SPL queries (sync + async)
    - Normalize results
    - Persist MCP transactions
    - Provide unified logging for observability
    """

    TOOL_NAME = "generic"

    def __init__(self, splunk_service=None):
        self._service = splunk_service

    # =====================================================
    # SPLUNK CONNECTION (LAZY LOADING)
    # =====================================================
    @property
    def service(self):
        if self._service is None:
            logger.info(f"[{self.TOOL_NAME}] 🔌 Connecting to Splunk...")

            try:
                self._service = connect()
                logger.success(f"[{self.TOOL_NAME}] ✅ Splunk connection established")
            except Exception as e:
                logger.exception(f"[{self.TOOL_NAME}] ❌ Splunk connection failed")
                raise ConnectionError(f"Splunk connection failed: {e}")

        return self._service

    # =====================================================
    # ASYNC EXECUTION (NON-BLOCKING PIPELINE)
    # =====================================================
    async def execute_async(self, query: str):
        logger.info(f"[{self.TOOL_NAME}] 🔍 Async execution started")
        logger.debug(f"[{self.TOOL_NAME}] SPL: {query}")

        try:
            loop = asyncio.get_running_loop()

            logger.info(f"[{self.TOOL_NAME}] 📡 Sending query to Splunk")

            raw = await loop.run_in_executor(
                None,
                run_search,
                self.service,
                query
            )

            logger.info(f"[{self.TOOL_NAME}] 📥 Raw response received")

            result = normalize_response(raw)

            logger.info(f"[{self.TOOL_NAME}] 📊 Parsed {len(result)} events")

            if not result:
                logger.warning(f"[{self.TOOL_NAME}] ⚠️ Empty result set from Splunk")

            # Persist MCP transaction
            try:
                await loop.run_in_executor(
                    None,
                    MCPStore.save,
                    self.TOOL_NAME,
                    {"query": query, "results": result}
                )
                logger.debug(f"[{self.TOOL_NAME}] 💾 Stored MCP transaction")
            except Exception as e:
                logger.error(f"[{self.TOOL_NAME}] ❌ MCPStore write failed: {e}")

            logger.success(f"[{self.TOOL_NAME}] ✅ Async execution complete")

            return result

        except Exception as e:
            logger.exception(f"[{self.TOOL_NAME}] ❌ Async execution failed")
            return {
                "status": "error",
                "message": str(e),
                "results": []
            }

    # =====================================================
    # SYNC EXECUTION (DAEMON / PIPELINE USE)
    # =====================================================
    def execute(self, query: str):
        logger.info(f"[{self.TOOL_NAME}] 🔍 Sync execution started")
        logger.debug(f"[{self.TOOL_NAME}] SPL: {query}")

        try:
            logger.info(f"[{self.TOOL_NAME}] 📡 Querying Splunk")

            raw = run_search(self.service, query)

            logger.info(f"[{self.TOOL_NAME}] 📥 Response received")

            result = normalize_response(raw)

            logger.info(f"[{self.TOOL_NAME}] 📊 Parsed {len(result)} events")

            if not result:
                logger.warning(f"[{self.TOOL_NAME}] ⚠️ Empty result set (check SPL or indexes)")

            # Persist MCP transaction
            try:
                MCPStore.save(self.TOOL_NAME, {"query": query, "results": result})
                logger.debug(f"[{self.TOOL_NAME}] 💾 MCP transaction stored")
            except Exception as e:
                logger.error(f"[{self.TOOL_NAME}] ❌ MCPStore save failed: {e}")

            logger.success(f"[{self.TOOL_NAME}] ✅ Execution complete")

            return result

        except Exception as e:
            logger.exception(f"[{self.TOOL_NAME}] ❌ Execution crashed")
            return {
                "status": "error",
                "results": [],
                "message": str(e)
            }