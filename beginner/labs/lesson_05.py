text = "call maya"
vocabulary = sorted(set(text))
to_id = {char: i for i, char in enumerate(vocabulary)}
ids = [to_id[char] for char in text]
recovered = "".join(vocabulary[i] for i in ids)
print(ids)
print(recovered)
assert recovered == text
