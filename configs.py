from elasticsearch import Elasticsearch

es_index = "products-v2"
es_client = Elasticsearch("http://localhost:9200")
batch_size = 1000