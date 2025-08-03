import pandas as pd
import math
from time import time
from core.configs import (
  batch_size,
  file_name
)
from helpers.process_data import process_data
from helpers.payload_constructor import prepare_payload
from helpers.request_executor import send_request

# Read file
dataframe = pd.read_csv(f"input/{file_name}", encoding="utf8")

# Updatable columns (the column 'id' is not needed here)
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
  
  prepare_payload(row, doc, request_body_ndjson)
  
  if((index+1) % batch_size == 0):
    send_request(request_body_ndjson)
  
  current_percentage = math.ceil(((index+1) / totalCount) * 100)
  if(current_percentage % 5 == 0 and current_percentage != last_percentage):
    print(f"Progress {current_percentage}%")
    last_percentage = current_percentage

# Upload the remaining
# es_client.bulk(index=es_index, body=request_body_ndjson)
send_request(request_body_ndjson)

print(f"\nElapsed time {round(time() - start_time, 2)} seconds")