import time
import splunklib.client as splunk_client
import splunklib.results as results

from src.splunk.config import (
    SPLUNK_HOST,
    SPLUNK_PORT,
    SPLUNK_USERNAME,
    SPLUNK_PASSWORD,
    validate_config,
)


def connect():
    validate_config()

    return splunk_client.connect(
        host=SPLUNK_HOST,
        port=SPLUNK_PORT,
        username=SPLUNK_USERNAME,
        password=SPLUNK_PASSWORD,
    )


def run_search(service, query, timeout=30):
    """
    Execute SPL query and return structured results with metadata stripping.
    """

    job = service.jobs.create(query)

    start = time.time()

    try:
        while not job.is_done():
            if time.time() - start > timeout:
                job.cancel()
                raise TimeoutError("Splunk query timed out")
            time.sleep(1)

        reader = results.ResultsReader(job.results())

        output = []

        # Internal Splunk metadata fields to strip out for cleaner down-stream processing
        internal_metadata = {'_cd', '_bkt', '_si', '_serial', '_indextime'}

        for item in reader:
            if isinstance(item, dict):
                # Strip internal metadata fields to prevent LLM token bloating
                cleaned_item = {k: v for k, v in item.items() if k not in internal_metadata}
                output.append(cleaned_item)

        return {
            "status": "success",
            "count": len(output),
            "data": output
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "data": []
        }

    finally:
        try:
            job.cancel()
        except:
            pass