def execute(proposal, confirmed, permissions):
    if proposal.get("tool") != "reminders.propose":
        return "unknown tool"
    if not proposal.get("text"):
        return "missing reminder text"
    if "reminders.write" not in permissions:
        return "permission required"
    if not confirmed:
        return "confirmation required"
    return "mock reminder accepted"

p = {"tool": "reminders.propose", "text": "Call Maya"}
print(execute(p, False, {"reminders.write"}))
print(execute(p, True, {"reminders.write"}))
