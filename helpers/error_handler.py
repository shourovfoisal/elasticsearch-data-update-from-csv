from helpers.log import write_log_file
from typing import Dict, Any, TypeAlias

BulkResponse: TypeAlias = Dict[str, Any]

def handle_error(response: BulkResponse):
  for item in response["items"]:
    operation_description = item["update"]
    
    if "error" in operation_description:
      item_id = operation_description["_id"]
      error_description = operation_description["error"]
      error_type = error_description["type"]
      error_reason = error_description["reason"]
      
      write_log_file(f"Error occured with document id {item_id}\nError type: {error_type}\nError reason: {error_reason}")
      # print(f"\nError occured with document id {item_id}")
      # print(f"Error type: {error_type}")
      # print(f"Error reason: {error_reason}")
      