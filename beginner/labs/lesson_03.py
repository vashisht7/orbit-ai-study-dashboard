import math

def softmax(scores, temperature=1.0):
    scaled = [s / temperature for s in scores]
    largest = max(scaled)
    values = [math.exp(s - largest) for s in scaled]
    return [v / sum(values) for v in values]

print([round(p, 3) for p in softmax([2, 1, 0])])
print([round(p, 3) for p in softmax([2, 1, 0], 2)])
