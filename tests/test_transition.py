"""Invariant 4: the transition.

After position 12 comes position 1 with one extra cycle. Position 0 never
occurs. The 1-based model is checked against an independent oracle for
q = 7, 9, 12, 24, 60.
"""
from __future__ import annotations

import pytest

from rd.cycle import Cycle


# ----------------------------------------------------------- oracle
def oracle_position(t: int, q: int) -> int:
    """Step-by-step simulation: no formula, just counting.

    Start at position 1. Every q steps the position resets to 1.
    """
    pos = 1
    for _ in range(t - 1):
        pos += 1
        if pos > q:
            pos = 1
    return pos


def oracle_cycles(t: int, q: int) -> int:
    """Number of complete cycles elapsed before step t, by simulation."""
    pos = 1
    cycles = 0
    for _ in range(t - 1):
        pos += 1
        if pos > q:
            pos = 1
            cycles += 1
    return cycles


# -------------------------------------------------- specific values
@pytest.mark.parametrize("t,expected", [
    (1, 1),
    (11, 11),
    (12, 12),
    (13, 1),
    (23, 11),
    (24, 12),
    (25, 1),
    (36, 12),
    (37, 1),
])
def test_known_positions(t: int, expected: int) -> None:
    assert Cycle(12).position(t) == expected


def test_position_is_never_zero() -> None:
    c = Cycle(12)
    for t in range(1, 1_001):
        assert 1 <= c.position(t) <= 12


def test_index_may_be_zero() -> None:
    """The smallest coefficient A0 can be 0 at exact cycle boundaries."""
    c = Cycle(12)
    assert c.index(12) == 0
    assert c.index(24) == 0
    assert c.index(13) == 1
    assert c.index(25) == 1


def test_cycles_count() -> None:
    c = Cycle(12)
    assert c.cycles(12) == 0
    assert c.cycles(13) == 1
    assert c.cycles(24) == 1
    assert c.cycles(25) == 2


@pytest.mark.slow
def test_transition_sweep() -> None:
    """T from 1 to 100,000: position always 1..12, never 0."""
    c = Cycle(12)
    for t in range(1, 100_001):
        assert 1 <= c.position(t) <= 12, f"position out of range at T={t}"


# ------------------------------------------------------ oracle parity
@pytest.mark.slow
@pytest.mark.parametrize("q", [7, 9, 12, 24, 60])
def test_oracle_position_parity(q: int) -> None:
    """The 1-based formula agrees with the oracle for every q in the series."""
    c = Cycle(q)
    for t in range(1, 2_001):
        assert c.position(t) == oracle_position(t, q), f"q={q}, t={t}"


@pytest.mark.slow
@pytest.mark.parametrize("q", [7, 9, 12, 24, 60])
def test_oracle_cycles_parity(q: int) -> None:
    c = Cycle(q)
    for t in range(1, 1_001):
        assert c.cycles(t) == oracle_cycles(t, q), f"q={q}, t={t}"


@pytest.mark.parametrize("q", [7, 9, 12, 24, 60])
def test_transition_count(q: int) -> None:
    """Number of end-to-beginning transitions in 1..t."""
    c = Cycle(q)
    for t in [q, q + 1, 2 * q, 2 * q + 1, 10 * q]:
        assert c.transition_count(t) == t // q


def test_decompose_returns_both_answers() -> None:
    c = Cycle(12)
    d = c.decompose(25)
    assert d.cycles == 2
    assert d.position == 1


def test_cycle_length_one() -> None:
    """Edge case: q = 1 means every step is position 1."""
    c = Cycle(1)
    for t in range(1, 11):
        assert c.position(t) == 1
        assert c.cycles(t) == t - 1


def test_invalid_cycle_raises() -> None:
    with pytest.raises(ValueError):
        Cycle(0)
    with pytest.raises(ValueError):
        Cycle(12, p=24)      # 24 is not ≡ 1 (mod 12)
    with pytest.raises(ValueError):
        Cycle(12, p=0)
