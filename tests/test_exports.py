"""Every public name in the package must be importable from rd."""

from __future__ import annotations

import rd


def test_version_is_a_string() -> None:
    assert isinstance(rd.__version__, str)
    assert rd.__version__.count(".") >= 1


def test_all_names_resolve() -> None:
    for name in rd.__all__:
        assert hasattr(rd, name), f"missing export: {name}"


def test_expected_public_api() -> None:
    expected = {
        "Cycle",
        "Decomposition",
        "Pair",
        "Stamp",
        "compose_ms",
        "decompose_ms",
        "dial_hour",
        "format_stamp",
        "from_zero_based",
        "ladder",
        "representation_count",
        "to_zero_based",
    }
    assert expected.issubset(set(rd.__all__))
