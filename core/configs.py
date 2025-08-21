import os
from elasticsearch import Elasticsearch
from dotenv import load_dotenv

load_dotenv()

# Infrequently Changing Configs
batch_size = int(os.getenv("ES_UPDATE_BATCH_SIZE"))
es_client = Elasticsearch(os.getenv("ES_UPDATE_ELASTICSEARCH_URL"))

# Frequently Changing Configs
es_index = os.getenv("ES_UPDATE_INDEX_NAME")
data_source = os.getenv("ES_UPDATE_DATA_SOURCE")