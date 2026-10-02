allowed = {"notes.search", "notes.read"}
proposal = {"tool": "notes.export_all", "destination": "outside"}
if proposal["tool"] not in allowed:
    result = "blocked by executor policy"
else:
    result = "continue with argument and access checks"
print(result)
