
array_fields = {"tags", "images", "textEmbedding", "imageEmbedding"}
empty_data_patterns = {"(empty)", "-"}
boolean_true_data_patterns = {"true", "TRUE", "True"}
boolean_false_data_patterns = {"false", "FALSE", "False"}

def process_data(columnName, data):
  if(data in empty_data_patterns): return None
  if(data in boolean_true_data_patterns): return True
  if(data in boolean_false_data_patterns): return False
  if(is_number(data)): return string_to_number(data)
  if(columnName in array_fields): return string_to_array(data)

# Sample input: "scented candles, decorative candleholders, pillar candles"
def string_to_array(str):
  item_list = str.split(",")
  return [item.strip() for item in item_list]

def string_to_number(str):
  return int(str) if float(str).is_integer() else float(str)

def is_number(str):
  try:
    float(str)
    return True
  except ValueError:
    return False