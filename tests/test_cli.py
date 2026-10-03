"""Tests for the command line interface in rd.__main__."""
from __future__ import annotations

import pytest

from rd.__main__ import main


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


def test_system_mode_success(capsys: pytest.CaptureFixture[str]) -> None:
    code = main(["--system", "25,12", "500"])
    out = capsys.readouterr().out
    assert code == 0
    assert "R(500) = 2" in out
    assert "(8, 25)" in out
    assert "(20, 0)" in out


def test_system_mode_no_representation(
    capsys: pytest.CaptureFixture[str],
) -> None:
    code = main(["--system", "25,12", "263"])
    out = capsys.readouterr().out
    assert code == 1
    assert "geen representatie" in out


def test_system_mode_malformed(
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


def test_missing_mode_argument() -> None:
    with pytest.raises(SystemExit):
        main(["500"])


def test_mutually_exclusive_modes() -> None:
    with pytest.raises(SystemExit):
        main(["--ms", "--system", "25,12", "500"])


def test_default_invocation(capsys: pytest.CaptureFixture[str]) -> None:
    """Without arguments argparse prints help and exits."""
    with pytest.raises(SystemExit):
        main([])
