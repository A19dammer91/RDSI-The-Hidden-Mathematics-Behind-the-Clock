"""Invariant 3: clock uniqueness, plus full coverage of cascade.py."""

from __future__ import annotations

import random

import pytest

from rd.cascade import (
    MS_DAY,
    MS_HOUR,
    MS_MIN,
    MS_SEC,
    Stamp,
    compose_ms,
    decompose_ms,
    dial_hour,
    format_stamp,
)

# --------------------------------------------------------- constants


def test_constants() -> None:
    assert MS_SEC == 1_000
    assert MS_MIN == 60_000
    assert MS_HOUR == 3_600_000
    assert MS_DAY == 86_400_000


# --------------------------------------------------- worked examples


def test_worked_example() -> None:
    """The headline value from the RDSI paper."""
    stamp = decompose_ms(45_296_789)
    assert stamp == Stamp(days=0, hours=12, minutes=34, seconds=56, millis=789)
    assert format_stamp(stamp) == "0 d 12:34:56.789"


def test_3661_seconds() -> None:
    """3,661 seconds should read as 1:01:01 on the dial."""
    stamp = decompose_ms(3_661_000)
    assert (stamp.hours, stamp.minutes, stamp.seconds) == (1, 1, 1)


# ------------------------------------------------------- round trips


def test_round_trip_at_zero() -> None:
    stamp = decompose_ms(0)
    assert stamp == Stamp(0, 0, 0, 0, 0)
    assert compose_ms(stamp) == 0
    assert format_stamp(stamp) == "0 d 12:00:00.000"


def test_round_trip_at_one_day_minus_one() -> None:
    """The last millisecond of a day."""
    t = MS_DAY - 1
    stamp = decompose_ms(t)
    assert (stamp.days, stamp.hours, stamp.minutes, stamp.seconds, stamp.millis) == (
        0,
        23,
        59,
        59,
        999,
    )
    assert compose_ms(stamp) == t


def test_round_trip_at_exactly_one_day() -> None:
    t = MS_DAY
    stamp = decompose_ms(t)
    assert stamp.days == 1
    assert (stamp.hours, stamp.minutes, stamp.seconds, stamp.millis) == (0, 0, 0, 0)
    assert compose_ms(stamp) == t


def test_negative_input_is_allowed() -> None:
    """Timestamps before the epoch decompose with negative days."""
    stamp = decompose_ms(-1)
    assert stamp.days == -1
    assert (stamp.hours, stamp.minutes, stamp.seconds, stamp.millis) == (
        23,
        59,
        59,
        999,
    )
    assert compose_ms(stamp) == -1


# ------------------------------------------------------------ dial


@pytest.mark.parametrize(
    "h24,expected",
    [
        (0, 12),  # midnight shows as 12
        (1, 1),
        (11, 11),
        (12, 12),  # noon shows as 12
        (13, 1),
        (23, 11),
    ],
)
def test_dial_hour(h24: int, expected: int) -> None:
    assert dial_hour(h24) == expected


def test_dial_hour_never_zero() -> None:
    for h in range(0, 24):
        assert 1 <= dial_hour(h) <= 12


# --------------------------------------------------- Stamp validation


def test_stamp_rejects_hours() -> None:
    with pytest.raises(ValueError):
        Stamp(0, 24, 0, 0, 0)
    with pytest.raises(ValueError):
        Stamp(0, -1, 0, 0, 0)


def test_stamp_rejects_minutes() -> None:
    with pytest.raises(ValueError):
        Stamp(0, 0, 60, 0, 0)
    with pytest.raises(ValueError):
        Stamp(0, 0, -1, 0, 0)


def test_stamp_rejects_seconds() -> None:
    with pytest.raises(ValueError):
        Stamp(0, 0, 0, 60, 0)
    with pytest.raises(ValueError):
        Stamp(0, 0, 0, -1, 0)


def test_stamp_rejects_millis() -> None:
    with pytest.raises(ValueError):
        Stamp(0, 0, 0, 0, 1000)
    with pytest.raises(ValueError):
        Stamp(0, 0, 0, 0, -1)


# ------------------------------------------------------- slow sweeps


@pytest.mark.slow
def test_uniqueness_sweep_two_days() -> None:
    """Every millisecond in two days round-trips."""
    for t in range(0, 2 * MS_DAY):
        assert compose_ms(decompose_ms(t)) == t, f"round-trip failed at T={t}"


@pytest.mark.slow
def test_uniqueness_random_sample() -> None:
    """200,000 random instants round-trip."""
    rng = random.Random(2026)
    for _ in range(200_000):
        t = rng.randrange(0, 10 * MS_DAY)
        assert compose_ms(decompose_ms(t)) == t
