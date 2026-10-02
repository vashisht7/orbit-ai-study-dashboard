expected = ["reminder", "clarify", "note", "cancel"]
observed = ["reminder", "reminder", "note", "cancel"]
correct = [a == b for a, b in zip(expected, observed)]
print(sum(correct) / len(correct))  # 0.75
for i, ok in enumerate(correct):
    if not ok:
        print("Inspect case", i, expected[i], observed[i])
