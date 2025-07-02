import pandas as pd
from elasticsearch import Elasticsearch
from process_data import process_data

# Change here
es_index = "products-v2"

# Client
es = Elasticsearch("http://localhost:9200")

# Read file
dataframe = pd.read_csv("input/data.csv", nrows=100, encoding="utf8")

# Updatable columns
columns = dataframe.columns.tolist()
if "id" in columns: columns.remove("id")

for index, row in dataframe.iterrows():
  doc = dict()
  
  for column in columns:
    doc[column]=process_data(column, row[column])
  
  payload = {"doc": doc}
  
  es.update(index=es_index, id=row['id'].replace(",", ""), body=payload)