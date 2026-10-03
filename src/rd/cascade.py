"""Clock cascade: positional divisibility chain [days, 24, 60, 60, 1000].

The clock is *internally* 0-based (hours 0..23, minutes 0..59, ...).
That is correct for a positional system and it is what makes the
decomposition unique. The 1-based model only applies to the *dial*,
which is a display layer, not an arithmetic one.

See §4.1 and §5.3 of the paper.
"""
from __future__ import annotations

from dataclasses import dataclass

__all__ = [
    "MS_DAY",
    "MS_HOUR",
    "MS_MIN",
    "MS_SEC",
    "Stamp",
    "compose_ms",
    "decompose_ms",
    "dial_hour",
    "format_stamp",
]

MS_SEC = 1_000
MS_MIN = 60_000
MS_HOUR = 3_600_000
MS_DAY = 86_400_000


@dataclass(frozen=True, slots=True)
class Stamp:
    """A decomposed timestamp.

    ``hours``, ``minutes``, ``seconds`` are 0-based (positional).
    Use :func:`dial_hour` for the 1-based dial representation.
    """

    days: int
    hours: int      # 0..23
    minutes: int    # 0..59
    seconds: int    # 0..59
    millis: int     # 0..999

    def __post_init__(self) -> None:
        if not 0 <= self.hours < 24:
            raise ValueError(f"hours buiten bereik: {self.hours}")
        if not 0 <= self.minutes < 60:
            raise ValueError(f"minutes buiten bereik: {self.minutes}")
        if not 0 <= self.seconds < 60:
            raise ValueError(f"seconds buiten bereik: {self.seconds}")
        if not 0 <= self.millis < 1_000:
            raise ValueError(f"millis buiten bereik: {self.millis}")


def decompose_ms(t: int) -> Stamp:
    """Milliseconds since midnight → :class:`Stamp`.

    For ``t = 45_296_789`` this returns ``0 d 12:34:56.789``, as in §5.4.
    Negative ``t`` is allowed and yields negative ``days``.
    """
    d, r = divmod(t, MS_DAY)
    h, r = divmod(r, MS_HOUR)
    m, r = divmod(r, MS_MIN)
    s, ms = divmod(r, MS_SEC)
    return Stamp(d, h, m, s, ms)


def compose_ms(s: Stamp) -> int:
    """Inverse of :func:`decompose_ms`."""
    return (
        s.days * MS_DAY
        + s.hours * MS_HOUR
        + s.minutes * MS_MIN
        + s.seconds * MS_SEC
        + s.millis
    )


def dial_hour(h24: int) -> int:
    """12-hour dial position, 1..12. Never returns 0.

    ``0 -> 12``, ``1 -> 1``, ``12 -> 12``, ``13 -> 1``, ``23 -> 11``.
    Branch-free, verified by ``tests/test_branchless.py``.
    """
    return (h24 - 1) % 12 + 1


def format_stamp(s: Stamp) -> str:
    """``0 d 12:34:56.789`` — the readable form from §4.3.

    The hour field uses the 1-based dial, so ``0`` shows as ``12``.
    """
    return (
        f"{s.days} d "
        f"{dial_hour(s.hours):02d}:"
        f"{s.minutes:02d}:"
        f"{s.seconds:02d}."
        f"{s.millis:03d}"
    )
