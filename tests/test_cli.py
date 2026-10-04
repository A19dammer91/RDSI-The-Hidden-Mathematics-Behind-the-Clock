"""Tests for the command line interface in rd.__main__."""
from __future__ import annotations

import pytest

from rd.__main__ import main

# ---------------------------------------------------------------- ms mode

def test_ms_mode(capsys: pytest.CaptureFixture[str]) -> None:
    code = main(["--ms", "45296789"])
    out = capsys.readouterr().out
    assert code == 0
    assert out.strip() == "0 d 12:34:56.789"


def test_ms_mode_zero(capsys: pytest.CaptureFixture[str]) -> None:
    code = main(["--ms", "0"])
    out = capsys.readouterr().out
    assert code == 0
    assert out.strip() == "0 d 12:00:00.000"


def test_ms_mode_one_day(capsys: pytest.CaptureFixture[str]) -> None:
    code = main(["--ms", "86400000"])
    out = capsys.readouterr().out
    assert code == 0
    assert out.strip() == "1 d 12:00:00.000"


# ------------------------------------------------------------ system mode

def test_system_mode_success(capsys: pytest.CaptureFixture[str]) -> None:
    code = main(["--system", "25,12", "500"])
    out = capsys.readouterr().out
    assert code == 0
    assert "R(500) = 2" in out
    assert "(8, 25)" in out
    assert "(20, 0)" in out


def test_system_mode_single_representation(
    capsys: pytest.CaptureFixture[str],
) -> None:
    code = main(["--system", "25,12", "264"])
    out = capsys.readouterr().out
    assert code == 0
    assert "R(264) = 1" in out


def test_system_mode_no_representation(
    capsys: pytest.CaptureFixture[str],
) -> None:
    code = main(["--system", "25,12", "263"])
    out = capsys.readouterr().out
    assert code == 1
    assert "geen representatie" in out


# ---------------------------------------------------- malformed arguments

def test_system_mode_missing_comma(
    capsys: pytest.CaptureFixture[str],
) -> None:
    code = main(["--system", "25", "500"])
    err = capsys.readouterr().err
    assert code == 2
    assert "--system verwacht de vorm P,Q" in err


def test_system_mode_non_numeric(
    capsys: pytest.CaptureFixture[str],
) -> None:
    code = main(["--system", "abc,12", "500"])
    err = capsys.readouterr().err
    assert code == 2
    assert "--system verwacht de vorm P,Q" in err


def test_system_mode_invalid_relation(
    capsys: pytest.CaptureFixture[str],
) -> None:
    code = main(["--system", "25,13", "500"])
    err = capsys.readouterr().err
    assert code == 2
    assert "ongeldig systeem" in err


# -------------------------------------------------------------- argparse

def test_missing_mode_argument() -> None:
    """Without --ms or --system, argparse exits with an error."""
    with pytest.raises(SystemExit):
        main(["500"])


def test_mutually_exclusive_modes() -> None:
    """--ms and --system cannot be combined."""
    with pytest.raises(SystemExit):
        main(["--ms", "--system", "25,12", "500"])


def test_missing_positional() -> None:
    """The positional N/T argument is required."""
    with pytest.raises(SystemExit):
        main(["--ms"])


def test_no_arguments_at_all() -> None:
    """argparse prints usage and exits when nothing is given."""
    with pytest.raises(SystemExit):
        main([])
