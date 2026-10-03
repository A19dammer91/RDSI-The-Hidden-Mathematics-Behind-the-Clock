"""Invariant 4: the transition, plus full coverage of Cycle."""
from __future__ import annotations

import pytest

from rd.cycle import Cycle, Decomposition


def oracle_position(t: int, q: int) -> int:
    pos = 1
    for _ in range(t - 1):
        pos += 1
        if pos > q:
            pos = 1
    return pos


def oracle_cycles(t: int, q: int) -> int:
    pos = 1
    cycles = 0
    for _ in range(t - 1):
        pos += 1
        if pos > q:
            pos = 1
            cycles += 1
    return cycles


@pytest.mark.parametrize("t,expected", [
    (1, 1), (11, 11), (12, 12), (13, 1),
    (23, 11), (24, 12), (25, 1), (36, 12), (37, 1),
])
def test_known_positions(t: int, expected: int) -> None:
    assert Cycle(12).position(t) == expected


def test_position_is_never_zero() -> None:
    c = Cycle(12)
    for t in range(1, 1_001):
        assert 1 <= c.position(t) <= 12


def test_index_may_be_zero() -> None:
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


def test_decompose_returns_dataclass() -> None:
    d = Cycle(12).decompose(25)
    assert isinstance(d, Decomposition)
    assert d.cycles == 2
    assert d.position == 1


def test_walk_returns_tuple() -> None:
    assert Cycle(12).walk(25) == (2, 1)


def test_transition_count() -> None:
    c = Cycle(12)
    for t in [12, 13, 24, 25, 120]:
        assert c.transition_count(t) == t // 12


@pytest.mark.slow
def test_transition_sweep() -> None:
    c = Cycle(12)
    for t in range(1, 100_001):
        assert 1 <= c.position(t) <= 12


@pytest.mark.slow
@pytest.mark.parametrize("q", [7, 9, 12, 24, 60])
def test_oracle_position_parity(q: int) -> None:
    c = Cycle(q)
    for t in range(1, 2_001):
        assert c.position(t) == oracle_position(t, q)


@pytest.mark.slow
@pytest.mark.parametrize("q", [7, 9, 12, 24, 60])
def test_oracle_cycles_parity(q: int) -> None:
    c = Cycle(q)
    for t in range(1, 1_001):
        assert c.cycles(t) == oracle_cycles(t, q)


def test_cycle_length_one() -> None:
    c = Cycle(1)
    for t in range(1, 11):
        assert c.position(t) == 1
        assert c.cycles(t) == t - 1


def test_repr_without_p() -> None:
    assert repr(Cycle(12)) == "Cycle(q=12)"


def test_repr_with_p() -> None:
    assert repr(Cycle(12, p=25)) == "Cycle(p=25, q=12)"


def test_invalid_q_raises() -> None:
    with pytest.raises(ValueError):
        Cycle(0)
    with pytest.raises(ValueError):
        Cycle(-1)


def test_invalid_p_raises() -> None:
    with pytest.raises(ValueError):
        Cycle(12, p=24)      # 24 is not ≡ 1 (mod 12)
    with pytest.raises(ValueError):
        Cycle(12, p=0)
    with pytest.raises(ValueError):
        Cycle(12, p=-1)
