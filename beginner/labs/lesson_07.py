train = [("remind me at six", "reminder"),
         ("save this thought", "note")]
test = [("could you nudge me at six", "reminder"),
        ("save this thought", "note")]
def predict(text):
    return "reminder" if "remind" in text else "note"
def accuracy(rows):
    return sum(predict(x) == y for x, y in rows) / len(rows)
print(accuracy(train), accuracy(test))  # 1.0 0.5
