import time
import splunklib.client as splunk_client
import splunklib.results as results

from loguru import logger

from src.splunk.config import (
    SPLUNK_HOST,
    SPLUNK_PORT,
    SPLUNK_USERNAME,
    SPLUNK_PASSWORD,
    validate_config,
)

# =====================================================
# CONNECTION (SINGLE ENTRY POINT)
# =====================================================

def connect():
    """
    Creates and returns a Splunk service connection.
    This should ideally be reused (singleton via BaseTool).
    """
    validate_config()

    logger.info("🔌 Connecting to Splunk...")

    try:
        service = splunk_client.connect(
            host=SPLUNK_HOST,
            port=SPLUNK_PORT,
            username=SPLUNK_USERNAME,
            password=SPLUNK_PASSWORD,
        )

        logger.success("✅ Splunk connection established")
        return service

    except Exception as e:
        logger.exception("❌ Splunk connection failed")
        raise ConnectionError(f"Splunk connection failed: {e}")


# =====================================================
# FAST JOB-BASED SEARCH (OPTIMIZED)
# =====================================================

def run_search(service, query, timeout=20, poll_interval=0.2):
    """
    Optimized Splunk search using job polling.
    Faster than default SDK usage.
    """

    logger.info("🚀 Executing Splunk search job")
    logger.debug(f"SPL: {query}")

    job = service.jobs.create(query)
    start = time.time()

    try:
        # Faster polling loop
        while not job.is_done():
            if time.time() - start > timeout:
                job.cancel()
                logger.warning("⏱️ Splunk query timed out")
                raise TimeoutError("Splunk query timed out")

            time.sleep(poll_interval)

        logger.info("📥 Splunk job completed, fetching results")

        output = []

        reader = results.ResultsReader(job.results())

        for item in reader:
            if isinstance(item, dict):
                # Fast metadata stripping
                cleaned = {
                    k: v for k, v in item.items()
                    if not k.startswith("_")
                }
                output.append(cleaned)

        logger.info(f"📊 Parsed {len(output)} events")

        return {
            "status": "success",
            "count": len(output),
            "data": output
        }

    except Exception as e:
        logger.exception("❌ Splunk search failed")
        return {
            "status": "error",
            "message": str(e),
            "data": []
        }

    finally:
        try:
            job.cancel()
        except Exception:
            pass


# =====================================================
# ULTRA FAST MODE (EXPORT STREAMING)
# =====================================================

def run_search_fast(service, query):
    """
    Ultra-fast mode using Splunk export API.
    Best for SOC streaming pipelines.
    No job polling = lowest latency.
    """

    logger.info("⚡ Executing FAST export search")
    logger.debug(f"SPL: {query}")

    try:
        output = []

        for item in service.jobs.export(query):
            if isinstance(item, dict):
                cleaned = {
                    k: v for k, v in item.items()
                    if not k.startswith("_")
                }
                output.append(cleaned)

        logger.info(f"📊 Fast mode parsed {len(output)} events")

        return {
            "status": "success",
            "mode": "fast",
            "count": len(output),
            "data": output
        }

    except Exception as e:
        logger.exception("❌ Fast Splunk search failed")
        return {
            "status": "error",
            "message": str(e),
            "data": []
        }