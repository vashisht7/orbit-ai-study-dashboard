answers = ["Source: a real supporting passage", "source source source"]
def bad_reward(text):
    return text.lower().count("source")
for text in answers:
    print(bad_reward(text), text)
