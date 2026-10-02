import math

def cosine(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    length_a = math.sqrt(sum(x*x for x in a))
    length_b = math.sqrt(sum(x*x for x in b))
    return dot / (length_a * length_b)

print(round(cosine([1, 0], [1, 1]), 3))  # 0.707
print(round(cosine([1, 0], [3, 4]), 3))  # 0.600
