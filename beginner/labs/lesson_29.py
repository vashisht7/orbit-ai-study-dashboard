settings = {"learning_rate": 0.1, "steps": 5, "seed": 7}
trial = dict(settings)
trial["learning_rate"] = 0.01
changed = [key for key in settings if settings[key] != trial[key]]
print(changed)  # ['learning_rate']
assert len(changed) == 1
