
array_fields = {"tags", "images", "textEmbedding", "imageEmbedding"}
empty_data_patterns = {"(empty)", "-"}
boolean_true_data_patterns = {"true", "TRUE", "True"}
boolean_false_data_patterns = {"false", "FALSE", "False"}
no_conversion_needed = {"infinity", "inf", "+inf", "-inf", "+infinity", "-infinity"}

def process_data(columnName, data):
  if(data in empty_data_patterns): return handle_empty_data(data)
  if(data in boolean_true_data_patterns): return True
  if(data in boolean_false_data_patterns): return False
  if(is_number(data)): return string_to_number(data)
  if(columnName in array_fields): return string_to_array(data)
  return data

# Sample input: "scented candles, decorative candleholders, pillar candles"
def string_to_array(data):
  item_list = data.split(",")
  return [string_to_number(item.strip()) if is_number(item.strip()) else item.strip() for item in item_list]

def string_to_number(data):
  return int(data) if float(data).is_integer() else float(data)

def is_number(data):
  try:
    if data in no_conversion_needed: return False
    float(data)
    return True
  except ValueError:
    return False
  
def handle_empty_data(data):
  if data == "(empty)": return ""
  if data == "-": return None