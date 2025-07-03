import pandas as pd
import math
import os
import json
import sys
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
      response = es_client.bulk(index=es_index, body=request_body_ndjson)
      if response.get("errors"):
        for item in response["items"]:
          operation_description = item["update"]
          
          if "error" in operation_description:
            item_id = operation_description["_id"]
            error_description = operation_description["error"]
            error_type = error_description["type"]
            error_reason = error_description["reason"]
          
            print(f"\nError occured with document id {item_id}")
            print(f"Error type: {error_type}")
            print(f"Error reason: {error_reason}")
            
      request_body_ndjson.clear()
    except Exception as e:
      print("\nBulk upload exception")
      print(e)
      os.makedirs("error_json", exist_ok=True)
      file_path = os.path.join("error_json", "docs_with_error.json")
      with open(file_path, "w", encoding="utf-8") as outfile:
        outfile.writelines(json.dumps(request_body_ndjson, ensure_ascii=False) + "\n")
        outfile.write("\n")
      sys.exit()
  
  current_percentage = math.ceil(((index+1) / totalCount) * 100)
  if(current_percentage % 5 == 0 and current_percentage != last_percentage):
    print(f"Progress {current_percentage}%")
    last_percentage = current_percentage

# Upload the remaining
es_client.bulk(index=es_index, body=request_body_ndjson)

print(f"\nElapsed time {round(time() - start_time, 2)} seconds")