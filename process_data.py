
array_fields = {"tags", "images", "textEmbedding", "imageEmbedding"}
empty_data_patterns = {"(empty)", "-"}
no_conversion_needed = {"infinity", "inf", "+inf", "-inf", "+infinity", "-infinity", "Nan", "NaN", "nan"}

def process_data(columnName, data):
  try:
    if(data in empty_data_patterns): return handle_empty_data(data)
    if(isinstance(data, str) and is_number_as_string(data.replace(",", ""))): 
      return string_to_number(data.replace(",", "")) if ',' in data else string_to_number(data)
    if(columnName in array_fields): return string_to_array(data)
    return data
  except Exception as e:
    print(e)
    print(f"Error happened for column: {columnName} and data: {data}")

# Sample input: "scented candles, decorative candleholders, pillar candles"
def string_to_array(data):
  item_list = data.split(",")
  return [string_to_number(item.strip()) if is_number_as_string(item.strip()) else item.strip() for item in item_list]

def string_to_number(data):
  return int(data) if float(data).is_integer() else float(data)

def is_number_as_string(data):
  try:
    if data in no_conversion_needed: return False
    float(data)
    return True
  except ValueError:
    return False
  
def handle_empty_data(data):
  if data == "(empty)": return ""
  if data == "-": return None