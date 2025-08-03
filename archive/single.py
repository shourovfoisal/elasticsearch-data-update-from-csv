


#####################################################
# THIS SINGLE REQUEST FILE IS NOT MAINTAINED ANYMORE
#####################################################

import pandas as pd
import math
from time import time
from core.configs import es_index, es_client
from helpers.process_data import process_data

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

for index, row in dataframe.iterrows():
  doc = dict()
  for columnName in columnNames:
    doc[columnName]=process_data(columnName, row[columnName])
  
  payload = {"doc": doc}
  
  try:
    es_client.update(index=es_index, id=row['id'].replace(",", ""), body=payload)
  except:
    print(f"Error while updating document with id {row['id']}")
    print("Payload:")
    print(payload)
  
  current_percentage = math.ceil(((index+1) / totalCount) * 100)
  if(current_percentage % 5 == 0 and current_percentage != last_percentage):
    print(f"Progress {current_percentage}%")
    last_percentage = current_percentage

print(f"\nElapsed time {round(time() - start_time, 2)} seconds")