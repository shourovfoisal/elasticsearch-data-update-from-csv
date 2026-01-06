def save_checkpoint(index: int):
  with open("checkpoint.txt", "w") as f:
    f.write(str(index))

def load_checkpoint():
  try:
    with open("checkpoint.txt") as f:
      print("Resuming from checkpoint")
      return int(f.read())
  except:
    print("Checkpoint not found. Starting from the beginning.")
    return -1

def reset_checkpoint():
  with open("checkpoint.txt", "w") as f:
    f.write("")