"""Invariant 2: the ladder, plus full coverage of ladder.py."""
from __future__ import annotations

from itertools import pairwise

import pytest

from rd.ladder import (
    Pair,
    frobenius,
    ladder,
    representation_count,
)

P = 25
Q = 12


def brute_force_count(n: int, p: int, q: int) -> int:
    """Independent check: count by direct enumeration, no formula."""
    if n < 0:
        return 0
    total = 0
    a = 0
    while p * a <= n:
        if (n - p * a) % q == 0:
            total += 1
        a += 1
    return total


# ---------------------------------------------------------------- Pair

def test_pair_value() -> None:
    assert Pair(8, 25).value(25, 12) == 500


def test_pair_iter() -> None:
    a, b = Pair(8, 25)
    assert (a, b) == (8, 25)
    assert list(Pair(8, 25)) == [8, 25]


# -------------------------------------------------------------- ladder

@pytest.mark.parametrize("n", [500, 575, 0, 1, 100, 263, 264, 1000])
def test_known_values(n: int) -> None:
    for pair in ladder(n, P, Q):
        assert pair.value(P, Q) == n
        assert pair.b >= 0
        assert pair.a >= 0


def test_500_worked_example() -> None:
    """The worked example from the RDSI paper: N = 500."""
    pairs = ladder(500, P, Q)
    assert [(x.a, x.b) for x in pairs] == [(8, 25), (20, 0)]


def test_575_narrative_example() -> None:
    """The narrative example from the README: N = 575."""
    pairs = ladder(575, P, Q)
    assert [(x.a, x.b) for x in pairs] == [(11, 25), (23, 0)]


def test_negative_input_returns_empty() -> None:
    assert ladder(-1, P, Q) == []


def test_ladder_is_ordered() -> None:
    """Pairs come back with increasing A and decreasing B."""
    pairs = ladder(5000, P, Q)
    for left, right in pairwise(pairs):
        assert right.a > left.a
        assert right.b < left.b


def test_ladder_step_size() -> None:
    """Consecutive pairs differ by exactly +12 in A and -25 in B."""
    pairs = ladder(5000, P, Q)
    for left, right in pairwise(pairs):
        assert right.a - left.a == Q
        assert left.b - right.b == P


# ---------------------------------------------------------- frobenius

def test_frobenius_value() -> None:
    assert frobenius(P, Q) == 263


def test_frobenius_formula_holds_for_other_pairs() -> None:
    """The formula p*q - p - q applies to every p ≡ 1 (mod q)."""
    assert frobenius(13, 12) == 13 * 12 - 13 - 12
    assert frobenius(19, 9) == 19 * 9 - 19 - 9
    assert frobenius(10, 9) == 10 * 9 - 10 - 9


# --------------------------------------------- representation_count

def test_representation_count_negative() -> None:
    assert representation_count(-1, P, Q) == 0


def test_representation_count_at_boundary() -> None:
    assert representation_count(263, P, Q) == 0
    assert representation_count(264, P, Q) >= 1


# ------------------------------------------------- validation paths

def test_invalid_q_raises() -> None:
    with pytest.raises(ValueError):
        ladder(500, P, 0)
    with pytest.raises(ValueError):
        ladder(500, P, -1)
    with pytest.raises(ValueError):
        representation_count(500, P, 0)
    with pytest.raises(ValueError):
        frobenius(P, 0)


def test_invalid_p_raises() -> None:
    with pytest.raises(ValueError):
        ladder(500, 0, Q)
    with pytest.raises(ValueError):
        ladder(500, -1, Q)
    with pytest.raises(ValueError):
        representation_count(500, 0, Q)
    with pytest.raises(ValueError):
        frobenius(0, Q)


def test_invalid_relation_raises() -> None:
    with pytest.raises(ValueError):
        ladder(500, 25, 13)      # 25 is not ≡ 1 (mod 13)
    with pytest.raises(ValueError):
        representation_count(500, 25, 13)
    with pytest.raises(ValueError):
        frobenius(25, 13)


# ------------------------------------------------------- slow sweeps

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

