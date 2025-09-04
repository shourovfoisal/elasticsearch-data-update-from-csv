import os

add_upon_failure = bool(os.getenv("ES_ADD_DOCUMENT_IF_NOT_EXISTS"))

def prepare_payload(row, doc, request_body_ndjson):
  document_id = row['id'].replace(",", "")
  metadata = { "update": { "_id": document_id } }
  payload = {"doc": doc}
  
  if(add_upon_failure): payload['doc_as_upsert'] = True  # Add the document to the elasticsearch when the document id is not found
  
  request_body_ndjson.append(metadata)
  request_body_ndjson.append(payload)