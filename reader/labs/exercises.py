"""Three blank exercises. Reference answers: labs.py softmax and metrics,
and the attention chapter. Fill these before running exercise_checks.py.
"""


def stable_softmax(logits):
    raise NotImplementedError(
        "Subtract the maximum, exponentiate, normalize."
    )


def causal_mask(length):
    """Return a square bool array: True means a position is allowed."""
    raise NotImplementedError("Position i may read key positions j <= i.")


def recall_at_k(ranked, relevant, k):
    """Deduplicate IDs, then truncate. Empty relevant set returns None."""
    raise NotImplementedError(
        "Count distinct relevant hits / relevant items."
    )
