words = "refunds allowed within thirty days except customized products".split()
size, overlap = 5, 2
step = size - overlap
chunks = [" ".join(words[i:i+size])
          for i in range(0, len(words), step)]
print(chunks)
assert 0 <= overlap < size
