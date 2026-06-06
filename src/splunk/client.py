import time

import splunklib.client as splunk_client
import splunklib.results as results

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
    """"
    Execute SPL query and return list of dictionaries.
    """

    while not job.is_done():
        time.sleep(1)
    reader = results.ResultsReader(job.results())

    output =[]
    for item in reader:
        if isinstance(item,dict):
            output.append(item)
        
    
    return output