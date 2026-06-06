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
    Execute SPL query and return structured results.
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

        for item in reader:
            if isinstance(item, dict):
                output.append(item)

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