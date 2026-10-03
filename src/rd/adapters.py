"""Bridge between the 1-based cycle model and 0-based consumers.

The RD model is 1-based: dial positions run from 1 to q. Most software
is 0-based: index positions run from 0 to q-1. The two conversions
below are the only correct shifts, and they are branch-free.
"""
from __future__ import annotations

__all__ = [
    "from_zero_based",
    "to_zero_based",
]


def to_zero_based(position: int, q: int) -> int:
    """1..q to 0..q-1.

    12 -> 0 for q = 12. The value 0 means "end of cycle" in the
    0-based world; it is not a valid input for the 1-based model.

    Raises
    ------
    ValueError
        If q < 1.
    """
    if q < 1:
        raise ValueError(f"q >= 1 vereist, kreeg q={q}")
    return position % q


def from_zero_based(zero: int, q: int) -> int:
    """0..q-1 to 1..q.

    0 -> 12 for q = 12. Same expression as Cycle.position; that is
    not a coincidence, it is the only correct shift, and it is
    branch-free.

    Raises
    ------
    ValueError
        If q < 1.
    """
    if q < 1:
        raise ValueError(f"q >= 1 vereist, kreeg q={q}")
    return (zero - 1) % q + 1
