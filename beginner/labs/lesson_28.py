results = {"schema": 15, "intent": 13, "safe_action": 15}
cases = 15
for metric, passed in results.items():
    print(metric, f"{passed}/{cases}", f"{passed/cases:.1%}")
print("Next step: inspect the two intent failures.")
