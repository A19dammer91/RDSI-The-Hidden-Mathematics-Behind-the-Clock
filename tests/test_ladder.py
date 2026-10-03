"""Invariant 2: the ladder holds.

Every pair on the ladder satisfies 25A + 12B = N with B >= 0.
The count is compared against an independent brute-force enumeration
that does not use the ladder generator.
"""
from __future__ import annotations

import pytest

from rd.ladder import Pair, ladder, representation_count

P = 25
Q = 12


def brute_force_count(n: int, p: int, q: int) -> int:
    """Independent check: count by direct enumeration, no formula."""
    if n < 0:
        return 0
    total = 0
    a = 0
    while p * a <= n:
        rem = n - p * a
        if rem % q == 0:
            total += 1
        a += 1
    return total


@pytest.mark.parametrize("n", [500, 575, 0, 1, 100, 263, 264, 1000])
def test_known_values(n: int) -> None:
    """Spot checks against values worked out by hand."""
    for pair in ladder(n, P, Q):
        assert pair.value(P, Q) == n
        assert pair.b >= 0
        assert pair.a >= 0


def test_500_worked_example() -> None:
    """The worked example from the RDSI paper: N = 500."""
    pairs = ladder(500, P, Q)
    as_tuples = [(x.a, x.b) for x in pairs]
    assert as_tuples == [(8, 25), (20, 0)]


def test_575_narrative_example() -> None:
    """The narrative example from the README: N = 575."""
    pairs = ladder(575, P, Q)
    as_tuples = [(x.a, x.b) for x in pairs]
    assert as_tuples == [(11, 25), (23, 0)]


@pytest.mark.slow
def test_ladder_holds_sweep() -> None:
    """Every pair on every ladder up to N = 5,000 satisfies the equation."""
    for n in range(0, 5_001):
        for pair in ladder(n, P, Q):
            assert pair.value(P, Q) == n, f"ladder broken at N={n}"


@pytest.mark.slow
def test_count_matches_brute_force() -> None:
    """The fast counter agrees with an independent enumeration."""
    for n in range(0, 5_001):
        assert representation_count(n, P, Q) == brute_force_count(n, P, Q), \
            f"count mismatch at N={n}"


def test_ladder_is_ordered() -> None:
    """Pairs come back with increasing A and decreasing B."""
    pairs = ladder(5000, P, Q)
    for left, right in zip(pairs, pairs[1:]):
        assert right.a > left.a
        assert right.b < left.b


def test_ladder_step_size() -> None:
    """Consecutive pairs differ by exactly +12 in A and -25 in B."""
    pairs = ladder(5000, P, Q)
    for left, right in zip(pairs, pairs[1:]):
        assert right.a - left.a == Q
        assert left.b - right.b == P


def test_negative_input_returns_empty() -> None:
    assert ladder(-1, P, Q) == []


def test_invalid_system_raises() -> None:
    with pytest.raises(ValueError):
        ladder(500, 25, 13)      # 25 is not ≡ 1 (mod 13)
