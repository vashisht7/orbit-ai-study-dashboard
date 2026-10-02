"""Inspectable smoothed character bigram baseline; standard library only."""
import math
import random


def fit(text, alphabet, alpha=1.0):
    if alpha <= 0 or len(set(alphabet)) != len(alphabet):
        raise ValueError("Use positive smoothing and a unique alphabet.")
    index = {c: i for i, c in enumerate(alphabet)}
    counts = [[alpha for _ in alphabet] for _ in alphabet]
    for a, b in zip(text, text[1:]):
        counts[index[a]][index[b]] += 1
    return [[v / sum(row) for v in row] for row in counts]


def nll(text, alphabet, probabilities):
    if len(text) < 2:
        raise ValueError("At least one transition is required.")
    index = {c: i for i, c in enumerate(alphabet)}
    return -sum(math.log(probabilities[index[a]][index[b]])
                for a, b in zip(text, text[1:])) / (len(text) - 1)


def sample(start, alphabet, probabilities, length=30, seed=7):
    rng = random.Random(seed)
    result = start
    for _ in range(length):
        row = probabilities[alphabet.index(result[-1])]
        result += rng.choices(alphabet, weights=row)[0]
    return result


def checks():
    p = fit("ABABAC", "ABC")
    assert all(math.isclose(sum(row), 1) for row in p)
    assert p[0] == [1/6, 3/6, 2/6]
    assert p[2] == [1/3, 1/3, 1/3]
    expected = -(2 * math.log(.5) + 2 * math.log(.6)
                 + math.log(1/3)) / 5
    assert math.isclose(nll("ABABAC", "ABC", p), expected)
    return {"rows": p, "training_nll": expected,
            "sample": sample("A", "ABC", p)}


if __name__ == "__main__":
    print(checks())
