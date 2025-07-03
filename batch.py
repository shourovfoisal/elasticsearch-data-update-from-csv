import pandas as pd
import math
from time import time
from configs import es_index, es_client, batch_size
from process_data import process_data

# Read file
dataframe = pd.read_csv("input/data.csv", encoding="utf8")

# Updatable columns
columnNames = dataframe.columns.tolist()
if "id" in columnNames: columnNames.remove("id")

# Log purposes
totalCount = len(dataframe)
tenPercentOfTotalCount = int(totalCount/10)
start_time = time()
last_percentage = -1

request_body_ndjson = []
for index, row in dataframe.iterrows():
  doc = dict()
  for columnName in columnNames:
    doc[columnName]=process_data(columnName, row[columnName])
  
  document_id = row['id'].replace(",", "")
  metadata = { "update": { "_id": document_id } }
  payload = {"doc": doc}
  request_body_ndjson.append(metadata)
  request_body_ndjson.append(payload)
  
  if((index+1) % batch_size == 0):
    try:
      es_client.bulk(index=es_index, body=request_body_ndjson)
      request_body_ndjson.clear()
    except:
      print(f"Error while updating document with id {row['id']}")
      print("Payload:")
      print(payload)
  
  current_percentage = math.ceil(((index+1) / totalCount) * 100)
  if(current_percentage % 5 == 0 and current_percentage != last_percentage):
    print(f"Progress {current_percentage}%")
    last_percentage = current_percentage

# Upload the remaining
es_client.bulk(index=es_index, body=request_body_ndjson)

print(f"\nElapsed time {round(time() - start_time, 2)} seconds")