"""Diophantine ladder for a (p, q) system with p ≡ 1 (mod q).

For N = p*A + q*B with integer, non-negative A, B, the foundation
relation makes the smallest coefficient a single step:

    A0 = N mod q

and every further solution is reached by stepping +q in A and -p in B.
That is the ladder of the RDSI paper.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass

__all__ = [
    "Pair",
    "frobenius",
    "ladder",
    "representation_count",
]


@dataclass(frozen=True, slots=True)
class Pair:
    """One representation N = p*A + q*B."""

    a: int
    b: int

    def value(self, p: int, q: int) -> int:
        """Evaluate p*A + q*B."""
        return p * self.a + q * self.b

    def __iter__(self) -> Iterator[int]:
        yield self.a
        yield self.b


def _check_system(p: int, q: int) -> None:
    if q < 1:
        raise ValueError(f"q >= 1 required, got q={q}")
    if p <= 0:
        raise ValueError(f"p > 0 required, got p={p}")
    if (p - 1) % q != 0:
        raise ValueError(f"fundamentele relatie geschonden: p={p} ≢ 1 (mod {q})")


def ladder(n: int, p: int, q: int) -> list[Pair]:
    """All non-negative integer solutions of p*A + q*B = N.

    Returned in increasing A (equivalently: decreasing B). Empty when
    N is not representable.

    Examples
    --------
    >>> [(x.a, x.b) for x in ladder(500, 25, 12)]
    [(8, 25), (20, 0)]
    >>> ladder(1, 25, 12)
    []
    """
    _check_system(p, q)

    if n < 0:
        return []

    a0 = n % q
    out: list[Pair] = []
    k = 0
    while True:
        a = a0 + q * k
        remainder = n - p * a
        if remainder < 0:
            return out
        out.append(Pair(a, remainder // q))
        k += 1


def representation_count(n: int, p: int, q: int) -> int:
    """R(N): number of pairs on the ladder. Zero is a valid answer."""
    _check_system(p, q)

    if n < 0:
        return 0

    a0 = n % q
    if n < p * a0:
        return 0
    return (n - p * a0) // (p * q) + 1


def frobenius(p: int, q: int) -> int:
    """Largest integer not representable as p*A + q*B.

    For coprime p, q this is p*q - p - q. Coprimality is guaranteed
    by the foundation relation p ≡ 1 (mod q), which _check_system
    enforces: p = kq + 1 implies gcd(p, q) = gcd(1, q) = 1.
    """
    _check_system(p, q)
    return p * q - p - q
