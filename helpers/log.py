import os
from datetime import datetime

LOG_FOLDER = "logs"

def write_log(message):
  os.makedirs(LOG_FOLDER, exist_ok=True)
  file_path = os.path.join(LOG_FOLDER, "log.txt")
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  with open(file_path, "a", encoding="utf-8") as file:
    file.write(f"[{timestamp}]\n{message}\n\n")