"""Invariant 1: the foundation relation.

For every N from 264 onward the smallest coefficient A on the ladder
equals N mod 12. The value 263 is the Frobenius number of (25, 12):
the largest integer that has no representation at all.
"""
from __future__ import annotations

import pytest

from rd.ladder import frobenius, ladder

P = 25
Q = 12
FROBENIUS = 263      # 25*12 - 25 - 12
FOUNDATION = 264     # smallest representable integer: 24 * 11


def test_frobenius_value() -> None:
    assert frobenius(P, Q) == FROBENIUS


def test_263_has_no_representation() -> None:
    assert ladder(FROBENIUS, P, Q) == []


def test_264_is_the_first_representable() -> None:
    pairs = ladder(FOUNDATION, P, Q)
    assert pairs, "264 must have at least one representation"
    assert pairs[0].a == FOUNDATION % Q
    assert pairs[0].value(P, Q) == FOUNDATION


@pytest.mark.parametrize("n", range(FOUNDATION, FOUNDATION + 200))
def test_foundation_on_first_run(n: int) -> None:
    """The first 200 representable integers, each checked individually."""
    pairs = ladder(n, P, Q)
    assert pairs, f"N={n} must be representable"
    assert pairs[0].a == n % Q


@pytest.mark.slow
def test_foundation_sweep() -> None:
    """Full sweep: every N from 264 to 200,000."""
    for n in range(FOUNDATION, 200_001):
        pairs = ladder(n, P, Q)
        assert pairs[0].a == n % Q, f"foundation failed at N={n}"


@pytest.mark.slow
def test_all_non_representable() -> None:
    """Every N below the Frobenius number must be non-representable."""
    for n in range(0, FROBENIUS + 1):
        assert ladder(n, P, Q) == [], f"N={n} should not be representable"
