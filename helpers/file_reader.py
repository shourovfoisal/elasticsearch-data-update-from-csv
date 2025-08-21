import pandas as pd
from glob import glob

def read_file():
  csv_files = glob("input/*.csv")
  if not csv_files:
    raise FileNotFoundError("No CSV file found in the 'input/' directory")
  elif len(csv_files) > 1:
    raise RuntimeError("Multiple CSV files found in the 'input/' directory. Please keep one.")
  file_name = csv_files[0]
  return pd.read_csv(file_name, encoding="utf8", low_memory=False)