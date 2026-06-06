class BaseTool:
    def __init__(self, splunk_client):
        self.client = splunk_client
    
    def run(self,query:str):
        return self.client.run_query(query)
        