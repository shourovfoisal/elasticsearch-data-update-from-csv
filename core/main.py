import math
from time import time as time_func
from core.configs import batch_size
from helpers.process_data import process_data
from helpers.payload_constructor import prepare_payload # type: ignore
from helpers.request_executor import send_with_retry
from helpers.checkpoint_manager import save_checkpoint, load_checkpoint, reset_checkpoint
from helpers.log import write_log_file, clear_log_file, print_to_console
from helpers.file_reader import read_file
from typing import List, Dict, Any, TypeAlias
from pandas import DataFrame

BulkRequestBody: TypeAlias = Dict[str, Any]
NdjsonBody: TypeAlias = List[Dict[str, Any]]

def main():
  # Clear the log file before starting the program
  clear_log_file()

  # Read file
  dataframe: DataFrame = read_file()
  print_to_console("Dataframe read complete")

  # Updatable columns (the column 'id' is not needed here)
  columnNames = dataframe.columns.tolist()
  if "id" in columnNames: columnNames.remove("id")

  # Log purposes
  totalCount = len(dataframe)
  start_time = time_func()
  last_percentage = -1

  start_index = load_checkpoint()

  payload: NdjsonBody = []
  for row_number, (df_index, row) in enumerate(dataframe.iterrows()): # type: ignore
    
    if row_number <= start_index:  # type: ignore
        continue
    
    doc: BulkRequestBody = dict()
    for columnName in columnNames:
      doc[columnName]=process_data(columnName, row[columnName])
    
    prepare_payload(row, doc, payload) # type: ignore
    
    if((row_number+1) % batch_size == 0):
      print_to_console(f"Batch {row_number + 1}")
      send_with_retry(payload)
      
      # save the LAST successfully processed row
      save_checkpoint(row_number)
      payload.clear()
    
    current_percentage: float = math.ceil(((row_number + 1) / totalCount) * 100)
    if(current_percentage % 5 == 0 and current_percentage != last_percentage):
      write_log_file(f"Progress {current_percentage}%", True)
      last_percentage = current_percentage

  # Upload the remaining
  if(len(payload) > 0):
    send_with_retry(payload)
    reset_checkpoint()

  write_log_file(f"Elapsed time {round(time_func() - start_time, 2)} seconds", True)
  
if __name__ == "__main__":
  main()