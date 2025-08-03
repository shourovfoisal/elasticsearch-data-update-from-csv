from elasticsearch import Elasticsearch
from core.const import (
  DATA_SOURCE_PYTHON as PYTHON, 
  DATA_SOURCE_KIBANA as KIBANA, 
  DATA_SOURCE_JAVA as JAVA
)

es_index = "products-v1-1"
es_client = Elasticsearch("http://localhost:9200")
batch_size = 1000
data_source = KIBANA