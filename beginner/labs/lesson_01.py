text = "Remind me to call Maya tomorrow at 6 pm"
if "remind" in text.lower():
    proposal = {"intent": "reminder", "needs_review": True}
else:
    proposal = {"intent": "note", "needs_review": False}
print(proposal)
