batch, positions, features, vocabulary = 2, 4, 8, 10
ids = [[1, 3, 2, 0], [2, 1, 4, 3]]
logits_shape = (len(ids), len(ids[0]), vocabulary)
print(logits_shape)  # (2, 4, 10)
print("Scores for one final position:", vocabulary)
