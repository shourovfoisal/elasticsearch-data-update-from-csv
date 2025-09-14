import os
from helpers.process_data import process_data

add_upon_failure = bool(os.getenv("ES_ADD_DOCUMENT_IF_NOT_EXISTS"))

def prepare_payload(row, doc, request_body_ndjson):
  document_id = row['id'].replace(",", "")
  request_meta = { "update": { "_id": document_id } }
  request_body = {}
  
  if(add_upon_failure):
    request_body['doc_as_upsert'] = True  # Add the document to the elasticsearch when the document id is not found
    doc["id"] = process_data("id", document_id)
  
  request_body["doc"] = doc
  
  request_body_ndjson.append(request_meta)
  request_body_ndjson.append(request_body)