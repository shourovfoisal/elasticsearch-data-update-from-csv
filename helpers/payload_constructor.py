import os
from helpers.process_data import process_data
from typing import List, Dict, Any, TypeAlias, TYPE_CHECKING
from pandas import Series

NdjsonBody: TypeAlias = List[Dict[str, Any]]
BulkRequestMeta: TypeAlias = Dict[str, Any]
BulkRequestBody: TypeAlias = Dict[str, Any]

if TYPE_CHECKING:
    SeriesAny = Series[Any]
else:
    SeriesAny = Series

add_upon_failure = bool(os.getenv("ES_ADD_DOCUMENT_IF_NOT_EXISTS"))

def prepare_payload(row: SeriesAny, doc: BulkRequestBody, payload: NdjsonBody):
  document_id = row['id'].replace(",", "")
  request_meta: BulkRequestMeta = { "update": { "_id": document_id } }
  request_body: BulkRequestBody = {}
  
  if(add_upon_failure):
    request_body['doc_as_upsert'] = True  # Add the document to the elasticsearch when the document id is not found
    doc["id"] = process_data("id", document_id)
  
  request_body["doc"] = doc
  
  payload.append(request_meta)
  payload.append(request_body)