
array_fields = { "tags", "images", "textEmbedding", "imageEmbedding" }

def process_data(columnName, data):
  if(columnName in array_fields): return string_to_array(data)

# Sample input: "scented candles, decorative candleholders, pillar candles"
def string_to_array(str):
  item_list = str.split(",")
  return [item.strip() for item in item_list]