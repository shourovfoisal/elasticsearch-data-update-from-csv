import ast
import traceback
from core.configs import data_source
from core.const import (
  DATA_SOURCE_PYTHON as PYTHON, 
  DATA_SOURCE_JAVA as JAVA, 
  DATA_SOURCE_KIBANA as KIBANA
)
import pandas as pd
from helpers.log import write_log

string_array_fields = {"tags", "images"}
number_array_fields = {"textEmbedding", "imageEmbedding"}
empty_data_patterns = {"(empty)", "-"}
no_conversion_needed = {"infinity", "inf", "+inf", "-inf", "+infinity", "-infinity", "Nan", "NaN", "nan"}

def process_data(columnName, data):
  try:
    # Check empty data
    if(data in empty_data_patterns): return handle_empty_data(data)
    if(pd.isna(data)): return None
    
    if(columnName in number_array_fields):
      return [float(x) for x in data.split(",")]
    
    if(columnName in string_array_fields):
      return data.split(",")
    
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
    write_log(error_message)

def string_to_number(data):
  return int(data) if float(data).is_integer() else float(data)

def is_number_as_string(data):
  try:
    if data in no_conversion_needed: return False
    float(data)
    return True
  except ValueError:
    return False
  
def handle_empty_data(data):
  if data == "(empty)": return ""
  if data == "-": return None
  if data == "nan": return None