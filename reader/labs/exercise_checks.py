"""These checks intentionally fail until exercises.py is completed."""

import numpy as np
from exercises import stable_softmax, causal_mask, recall_at_k

p = np.asarray(stable_softmax([1000, 1001, 1002]))
assert np.isfinite(p).all() and np.isclose(p.sum(), 1)
assert np.allclose(p, [0.09003057, 0.24472847, 0.66524096])
assert np.array_equal(
    causal_mask(3),
    [[True, False, False], [True, True, False], [True, True, True]],
)
assert recall_at_k(["x", "a", "a", "b"], {"a", "c"}, 3) == 0.5
assert recall_at_k([], set(), 3) is None
print("Starter exercise checks passed.")
