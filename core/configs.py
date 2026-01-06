import os
import sys
from elasticsearch import Elasticsearch
from dotenv import load_dotenv # type: ignore

load_dotenv()

# Infrequently Changing Configs
batch_size_from_env = os.getenv("ES_UPDATE_BATCH_SIZE")
if(batch_size_from_env):
  batch_size = int(batch_size_from_env)

username = os.getenv("ES_USERNAME")
password = os.getenv("ES_PASSWORD")

es_client: Elasticsearch

if username and password:
  es_client = Elasticsearch(
    os.getenv("ES_UPDATE_ELASTICSEARCH_URL"), 
    basic_auth=(username,password), 
    verify_certs=False,
    ssl_show_warn=False,
    ssl_assert_hostname=False, # type: ignore
    ssl_assert_fingerprint=False, # type: ignore
    request_timeout=180
  )
else:
  es_client = Elasticsearch(os.getenv("ES_UPDATE_ELASTICSEARCH_URL"))

# Frequently Changing Configs
es_index = os.getenv("ES_UPDATE_INDEX_NAME")
if not es_index:
  sys.exit("ERROR: ES_UPDATE_INDEX_NAME is missing or empty!")

data_source = os.getenv("ES_UPDATE_DATA_SOURCE")
if not data_source:
  sys.exit("ERROR: ES_UPDATE_DATA_SOURCE is missing or empty!")