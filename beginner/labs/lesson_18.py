budget = 3
results = [[], [], ["supporting passage"]]
state = "searching"
for attempt in range(budget):
    evidence = results[attempt]
    if evidence:
        state = "ready to answer"
        break
else:
    state = "insufficient evidence"
print(state)
