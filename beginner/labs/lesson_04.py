import math
# Fixed teaching weights: this illustrates inference, not a trained Transformer.
vocabulary = ["I", "like", "tea"]
token_id = vocabulary.index("I")
embeddings = [[1.0, 0.5], [0.2, 0.8], [0.7, -0.1]]
hidden = embeddings[token_id]
output_weights = [[0.0, 0.0], [1.0, 2.0], [0.0, 2.0]]
logits = [sum(w * h for w, h in zip(row, hidden))
          for row in output_weights]
shifted = [math.exp(z - max(logits)) for z in logits]
probabilities = [value / sum(shifted) for value in shifted]
print("Token ID:", token_id)
print("Embedding:", hidden)
print("Logits:", logits)
print({token: round(p, 3) for token, p in zip(vocabulary, probabilities)})
print("Greedy next token:", vocabulary[probabilities.index(max(probabilities))])
