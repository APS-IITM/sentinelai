import asyncio
from loguru import logger
from src.splunk.client import run_search
from src.utils.formatter import normalize_response
from src.storage.mcp_store import MCPStore

class BaseTool:
    TOOL_NAME = "generic"

    def __init__(self, splunk_service=None):
        """
        Accepts a shared, global Splunk service instance (Singleton pattern).
        If none is provided, it falls back to a lazy-loading connection to prevent initialization bloat.
        """
        self._service = splunk_service

    @property
    def service(self):
        """Lazy-load the connection only when the tool is explicitly executed."""
        if self._service is None:
            from src.splunk.client import connect
            logger.info(f"🔌 [MCP Tool: {self.TOOL_NAME}] Opening shared Splunk service channel...")
            self._service = connect()
        return self._service

    async def execute_async(self, query: str):
        """
        Executes the Splunk search query inside a separate thread pool
        to prevent blocking the main asynchronous MCP event loop.
        """
        logger.info(f"🔍 [MCP Tool: {self.TOOL_NAME}] Executing automated threat hunt query...")
        
        try:
            # Run the synchronous Splunk SDK call inside an async executor block
            loop = asyncio.get_running_loop()
            raw = await loop.run_in_executor(None, run_search, self.service, query)
            
            # Normalize the returned dataset
            result = normalize_response(raw)
            logger.success(f"📊 [MCP Tool: {self.TOOL_NAME}] Query completed. Found {len(result)} matching rows.")

            # Automatically commit the structured transaction into the database
            # This is what feeds the Investigation Console dashboard!
            try:
                # Run the database write inside the executor pool as well
                await loop.run_in_executor(
                    None, 
                    MCPStore.save, 
                    self.TOOL_NAME, 
                    {"query": query, "results": result}
                )
                logger.debug(f"💾 [MCP Tool: {self.TOOL_NAME}] Transaction logged to mcp_store table.")
            except Exception as store_err:
                logger.error(f"⚠️ [MCP Tool: {self.TOOL_NAME}] Failed to update mcp_store cache: {str(store_err)}")

            return result

        except Exception as e:
            logger.exception(f"❌ [MCP Tool: {self.TOOL_NAME}] Execution crashed during search operations.")
            return {"status": "error", "message": f"Tool execution failed: {str(e)}", "results": []}

    def execute(self, query: str):
        """Synchronous wrapper fallback for legacy pipeline engines or test scripts."""
        return asyncio.run(self.execute_async(query))