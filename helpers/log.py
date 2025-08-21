import os
from datetime import datetime

LOG_FOLDER = "logs"
LOG_FILE = os.path.join(LOG_FOLDER, "log.txt")

def write_log(message, should_print=False):
  os.makedirs(LOG_FOLDER, exist_ok=True)
  
  timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
  
  log = f"[{timestamp}]\n{message}\n\n"
  
  if should_print: print("\n" + log)
  with open(LOG_FILE, "a", encoding="utf-8") as file:
    file.write(log)
    
def clear_log():
  if os.path.exists(LOG_FILE):
    open(LOG_FILE, "w", encoding="utf-8").close()