from core.configs import (
  es_client,
  es_index
)
from helpers.error_handler import handle_error
from helpers.exception_handler import handle_exception
from typing import List, Dict, Any, TypeAlias
from helpers.log import write_log_file
import time

NdjsonBody: TypeAlias = List[Dict[str, Any]]
BulkResponse: TypeAlias = Dict[str, Any]

def send_request(payload: NdjsonBody):
  try:
    response: BulkResponse = es_client.bulk(index=es_index, operations=payload) # type:ignore
    if response.get("errors"):
      handle_error(response)
  except Exception as e:
    handle_exception(e, payload)
    raise

def send_with_retry(payload: NdjsonBody, max_retries:int = 5):
    for attempt in range(1, max_retries + 1):
        try:
            send_request(payload)
            return
        except Exception as e:
            wait = 2 ** attempt
            write_log_file(f"Retry {attempt}/{max_retries} after error: {e}", True)
            time.sleep(wait)

    raise RuntimeError("Max retries exceeded")