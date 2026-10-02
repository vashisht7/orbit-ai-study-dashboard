supported = {"notes.search": {"query"}}
request = {"tool": "notes.search", "arguments": {"query": "Atlas"}}
name = request["tool"]
required = supported.get(name)
valid = required is not None and required <= request["arguments"].keys()
print(valid)  # True
