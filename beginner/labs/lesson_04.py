from collections import defaultdict, Counter
text = "hello hello"
counts = defaultdict(Counter)
for previous, following in zip(text, text[1:]):
    counts[previous][following] += 1

row = counts["l"]
total = sum(row.values())
print(dict(row))
print({char: count / total for char, count in row.items()})
