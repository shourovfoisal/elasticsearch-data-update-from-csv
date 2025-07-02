import pandas as pd
from configs import es_index, es_client
from process_data import process_data

# Read file
dataframe = pd.read_csv("input/data.csv", nrows=200, encoding="utf8")

# Updatable columns
columnNames = dataframe.columns.tolist()
if "id" in columnNames: columnNames.remove("id")

totalCount = len(dataframe)
tenPercentOfTotalCount = int(totalCount/10)

for index, row in dataframe.iterrows():
  doc = dict()
  for columnName in columnNames:
    doc[columnName]=process_data(columnName, row[columnName])
  
  payload = {"doc": doc}
  es_client.update(index=es_index, id=row['id'].replace(",", ""), body=payload)
  
  if((index + 1) % tenPercentOfTotalCount == 0): print(f"Progress {int(((index + 1) * 100) / totalCount)}%", )