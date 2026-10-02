stages = {
    "audio": "recorded waveform",
    "transcript": "Remind me to call Maya tomorrow at 6 pm",
    "intent": "reminder",
    "tool_proposal": "reminders.propose",
    "execution": "not attempted in this teaching example",
}
for stage, value in stages.items():
    print(stage + ":", value)
