def relu(x):
    return max(0.0, x)

def network(x):
    hidden = [relu(2*x - 1), relu(-x + 2)]
    return hidden[0] - hidden[1]

for x in [0, 1, 2, 3]:
    print(x, network(x))  # -2, 0, 3, 5
