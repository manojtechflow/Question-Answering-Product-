import subprocess
import time
import os
import traceback as tr
from haystack.document_stores import ElasticsearchDocumentStore
import random 
import string

def run_elastic_search():

    document_store=''
    try:
        # Path to the Elasticsearch executable
        elasticsearch_path = r'C:\Users\thota\Desktop\Project\Inference\elasticsearch-8.8.2\bin\elasticsearch.bat'

        # Start Elasticsearch server
        process = subprocess.Popen(elasticsearch_path, shell=True)
    except:
        print(tr.format_exc)
        pass
    # Wait for Elasticsearch to start (optional)
    # You can add a delay here if needed, for example:
    # time.sleep(5)

    # Check the process return code to ensure Elasticsearch started successfully
    if process.returncode is None:
        print("Elasticsearch server started successfully.")
    else:
        print("Failed to start Elasticsearch server.")
    #sleeping 30 seconds for running elastic search    
    time.sleep(30)

    # Get the host where Elasticsearch is running, default to localhost
    try:
        host = os.environ.get("ELASTICSEARCH_HOST", "localhost")
        print(host)
        index = "inf37"
        document_store = ElasticsearchDocumentStore(host=host, username="", password="", index=index)
        return document_store
    except:
        print(tr.format_exc())
        return ''

    