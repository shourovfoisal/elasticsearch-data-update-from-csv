import math
import sys
from time import time
from core.configs import batch_size, es_index
from helpers.process_data import process_data
from helpers.payload_constructor import prepare_payload
from helpers.request_executor import send_request
from helpers.log import write_log
from helpers.file_reader import read_file

def main():
  # Check if index name is provided
  if not es_index.strip():
    print("Error: 'es_index' is not set. Please set it in the .env file.")
    sys.exit(1)

  # Read file
  dataframe = read_file()

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
      write_log(f"Progress {current_percentage}%", True)
      last_percentage = current_percentage

  # Upload the remaining
  send_request(request_body_ndjson)

  write_log(f"Elapsed time {round(time() - start_time, 2)} seconds", True)
  
if __name__ == "__main__":
  main()