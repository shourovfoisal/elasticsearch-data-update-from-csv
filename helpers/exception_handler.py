import sys
import traceback
from helpers.log import write_log_file
from typing import List, Dict, Any, TypeAlias

NdjsonBody: TypeAlias = List[Dict[str, Any]]

def handle_exception(e: Exception, payload: NdjsonBody):
  # print("\nBulk upload exception")
  # print(e)
  # os.makedirs("error_json", exist_ok=True)
  # file_path = os.path.join("error_json", "docs_with_error.json")
  # with open(file_path, "w", encoding="utf-8") as outfile:
  #   outfile.writelines(json.dumps(request_body_ndjson, ensure_ascii=False) + "\n")
  #   outfile.write("\n")
  error_message = f"[Exception] {type(e).__name__}: {e}"
  if payload:
    error_message += f"\n[Context] {repr(payload)}"
  error_message += f"\n[Traceback]\n{traceback.format_exc()}"

  # Write to log
  write_log_file(error_message)
  sys.exit()