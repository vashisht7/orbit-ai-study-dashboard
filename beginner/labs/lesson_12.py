probabilities = [0.60, 0.25, 0.10, 0.05]
top_p = 0.80
chosen, total = [], 0.0
for index, probability in enumerate(probabilities):
    chosen.append(index)
    total += probability
    if total >= top_p:
        break
print(chosen)  # [0, 1]
print([probabilities[i] / total for i in chosen])
