import heapq
scores = [(0.8, "note-A"), (0.3, "note-B"), (0.9, "note-C")]
print(heapq.nlargest(2, scores))
# [(0.9, 'note-C'), (0.8, 'note-A')]
