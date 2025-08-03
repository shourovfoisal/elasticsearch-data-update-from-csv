from core.configs import (
  es_client,
  es_index
)
from helpers.error_handler import handle_error
from helpers.exception_handler import handle_exception

def send_request(request_body_ndjson):
  try:
    response = es_client.bulk(index=es_index, body=request_body_ndjson)
    if response.get("errors"):
      handle_error(response)
    request_body_ndjson.clear()
  except Exception as e:
    handle_exception(e, request_body_ndjson)