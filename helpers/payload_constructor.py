
def prepare_payload(row, doc, request_body_ndjson):
  document_id = row['id'].replace(",", "")
  metadata = { "update": { "_id": document_id } }
  payload = {"doc": doc}
  request_body_ndjson.append(metadata)
  request_body_ndjson.append(payload)