import traceback
import pandas as pd
from helpers.log import write_log_file
from typing import Any

string_array_fields = {"tags", "images"}
number_array_fields = {"textEmbedding", "imageEmbedding"}
empty_data_patterns = {"(empty)", "-"}
no_conversion_needed = {"infinity", "inf", "+inf", "-inf", "+infinity", "-infinity", "Nan", "NaN", "nan"}

def process_data(columnName: str, data: Any):
  try:
    # Check empty data
    if(data in empty_data_patterns): return handle_empty_data(data)
    if(pd.isna(data)): return None
    
    if(columnName in number_array_fields):
      return [float(x) for x in data.split(",")]
    
    if(columnName in string_array_fields):
      return [item.strip() for item in data.split(",")]
    
    # Check if any single string value is actually a number in string format
    if(isinstance(data, str) and is_number_as_string(data.replace(",", ""))):
      return string_to_number(data.replace(",", "")) if ',' in data else string_to_number(data)
    
    return data
  
  except Exception as e:
    error_message = (
        f"Exception occurred in process_data:\n"
        f"Column: {columnName}\n"
        f"Data: {data}\n"
        f"Error: {str(e)}\n"
        f"Traceback:\n{traceback.format_exc()}"
    )
    write_log_file(error_message)

def string_to_number(data: str):
  return int(data) if float(data).is_integer() else float(data)

def is_number_as_string(data: str):
  try:
    if data in no_conversion_needed: return False
    float(data)
    return True
  except ValueError:
    return False
  
def handle_empty_data(data: str):
  if data == "(empty)": return ""
  if data == "-": return None
  if data == "nan": return None