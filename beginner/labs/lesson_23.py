trace = [
    {"stage": "retrieve", "ms": 20, "ok": True},
    {"stage": "generate", "ms": 120, "ok": True},
    {"stage": "validate", "ms": 2, "ok": False},
]
print("Total:", sum(x["ms"] for x in trace), "ms")
print("First failed stage:", next(x["stage"] for x in trace if not x["ok"]))
