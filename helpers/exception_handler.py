import os
import sys
import json

def handle_exception(e, request_body_ndjson):
  print("\nBulk upload exception")
  print(e)
  os.makedirs("error_json", exist_ok=True)
  file_path = os.path.join("error_json", "docs_with_error.json")
  with open(file_path, "w", encoding="utf-8") as outfile:
    outfile.writelines(json.dumps(request_body_ndjson, ensure_ascii=False) + "\n")
    outfile.write("\n")
  sys.exit()