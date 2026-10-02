x = [2.0, 1.0]
weights = [[3.0, -1.0], [0.0, 2.0]]
biases = [1.0, 0.0]
y = [sum(a*b for a, b in zip(x, row)) + bias
     for row, bias in zip(weights, biases)]
print(y)  # [6.0, 2.0]
