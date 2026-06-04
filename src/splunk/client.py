import splunklib.client as splunk_client

from src.splunk.config import(
    SPLUNK_HOST,
    SPLUNK_PORT,
    SPLUNK_USERNAME,
    SPLUNK_PASSWORD,
    validate_config,
    
)


def connect():
    validate_config()
    service = splunk_client.connect(
        host = SPLUNK_HOST,
        port = SPLUNK_PORT,
        username = SPLUNK_USERNAME,
        password = SPLUNK_PASSWORD,
    )

    return service

def run_search(service,query):
    job = service.jobs.create(query)

    while not job.is_done():
        pass

    return job.results()