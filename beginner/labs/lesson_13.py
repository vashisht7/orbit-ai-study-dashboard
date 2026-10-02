import json
raw = '{"intent":"reminder","hour":25}'
obj = json.loads(raw)
shape_ok = isinstance(obj.get("hour"), int)
meaning_ok = shape_ok and 0 <= obj["hour"] <= 23
print(shape_ok, meaning_ok)  # True False
