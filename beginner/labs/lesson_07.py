# A two-example batch. This is a real update of one scalar weight.
examples = [(1.0, 3.0), (2.0, 6.0)]
w = 1.0
learning_rate = 0.1
for step in range(3):
    losses = []
    gradients = []
    for x, target in examples:
        prediction = x * w                 # forward pass
        error = prediction - target
        losses.append(error ** 2)
        gradients.append(2 * error * x)     # backward calculation
    loss = sum(losses) / len(examples)
    gradient = sum(gradients) / len(examples)
    print(step, round(w, 3), round(loss, 3), round(gradient, 3))
    w = w - learning_rate * gradient        # optimizer update
