"""Tests for the 0-based to 1-based bridge."""
from __future__ import annotations

import pytest

from rd.adapters import from_zero_based, to_zero_based

# ------------------------------------------------------- from_zero_based

@pytest.mark.parametrize("zero,expected", [
    (0, 12),
    (1, 1),
    (11, 11),
    (12, 12),
    (13, 1),
    (24, 12),
    (25, 1),
])
def test_from_zero_based(zero: int, expected: int) -> None:
    assert from_zero_based(zero, 12) == expected


def test_from_zero_based_never_returns_zero() -> None:
    for q in (7, 9, 12, 24, 60):
        for z in range(0, 3 * q):
            assert from_zero_based(z, q) != 0


def test_from_zero_based_rejects_invalid_q() -> None:
    with pytest.raises(ValueError):
        from_zero_based(0, 0)
    with pytest.raises(ValueError):
        from_zero_based(0, -1)


# --------------------------------------------------------- to_zero_based

@pytest.mark.parametrize("position,expected", [
    (1, 1),
    (11, 11),
    (12, 0),
    (13, 1),
    (24, 0),
    (25, 1),
])
def test_to_zero_based(position: int, expected: int) -> None:
    assert to_zero_based(position, 12) == expected


def test_to_zero_based_rejects_invalid_q() -> None:
    with pytest.raises(ValueError):
        to_zero_based(1, 0)
    with pytest.raises(ValueError):
        to_zero_based(1, -1)


# ------------------------------------------------------------ round trip

def test_round_trip_for_all_cycle_lengths() -> None:
    """from_zero_based and to_zero_based are exact inverses."""
    for q in (7, 9, 12, 24, 60):
        for z in range(0, q):
            p = from_zero_based(z, q)
            assert 1 <= p <= q
            assert to_zero_based(p, q) == z


def test_matches_cycle_position() -> None:
    """from_zero_based is the same expression as Cycle.position."""
    from rd.cycle import Cycle

    for q in (7, 9, 12, 24, 60):
        c = Cycle(q)
        for t in range(1, 3 * q):
            zero = t % q
            assert from_zero_based(zero, q) == c.position(t)
