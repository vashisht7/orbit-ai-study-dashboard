lists = [["A", "B", "C"], ["B", "D", "A"]]
k0 = 60
scores = {}
for ranking in lists:
    for rank, doc in enumerate(ranking, start=1):
        scores[doc] = scores.get(doc, 0) + 1 / (k0 + rank)
print(sorted(scores, key=scores.get, reverse=True))
# B, A, D, C
