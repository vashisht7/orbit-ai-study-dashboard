w = 1.0
learning_rate = 0.1
for step in range(5):
    prediction = 2 * w
    loss = (prediction - 6) ** 2
    gradient = 4 * (prediction - 6)
    print(step, round(w, 4), round(loss, 4))
    w -= learning_rate * gradient
