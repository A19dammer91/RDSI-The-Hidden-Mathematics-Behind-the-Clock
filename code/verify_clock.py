#!/usr/bin/env python3
"""Verify the clock cascade [days, 24, 60, 60, 1000].

Checks:
  * round-trip: compose_ms(decompose_ms(T)) == T for every T in a range
  * bounds: hours < 24, minutes < 60, seconds < 60, millis < 1000
  * dial: dial_hour is always in 1..12 and never 0
  * the worked example 45,296,789 ms reads as 0 d 12:34:56.789

Exit code 0 on success, 1 on any failure.

Usage:
    python code/verify_clock.py [--days N] [--random N] [--quiet]
"""
from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rd.cascade import (  # noqa: E402
    MS_DAY,
    compose_ms,
    decompose_ms,
    dial_hour,
    format_stamp,
)

WORKED_EXAMPLE = 45_296_789
WORKED_STRING = "0 d 12:34:56.789"


def check_stamp(t: int) -> str | None:
    s = decompose_ms(t)
    if compose_ms(s) != t:
        return f"round-trip failed at T={t}"
    if not 0 <= s.hours < 24:
        return f"hours out of range at T={t}: {s.hours}"
    if not 0 <= s.minutes < 60:
        return f"minutes out of range at T={t}: {s.minutes}"
    if not 0 <= s.seconds < 60:
        return f"seconds out of range at T={t}: {s.seconds}"
    if not 0 <= s.millis < 1000:
        return f"millis out of range at T={t}: {s.millis}"
    return None


def run(days: int, random_n: int, quiet: bool) -> int:
    failures: list[str] = []

    if format_stamp(decompose_ms(WORKED_EXAMPLE)) != WORKED_STRING:
        failures.append(
            f"worked example: {format_stamp(decompose_ms(WORKED_EXAMPLE))} "
            f"!= {WORKED_STRING}"
        )

    total = days * MS_DAY
    for t in range(0, total):
        err = check_stamp(t)
        if err:
            failures.append(err)
            break
        if not quiet and t and t % 1_000_000 == 0:
            print(f"  ... {t:>12} checked", file=sys.stderr)

    if not failures:
        for h in range(0, 24):
            d = dial_hour(h)
            if not 1 <= d <= 12:
                failures.append(f"dial_hour({h}) = {d} out of range")

    if not failures and random_n > 0:
        rng = random.Random(2026)
        for _ in range(random_n):
            t = rng.randrange(0, 10 * MS_DAY)
            err = check_stamp(t)
            if err:
                failures.append(err)
                break

    if failures:
        print("FAIL", file=sys.stderr)
        for line in failures[:20]:
            print(f"  {line}", file=sys.stderr)
        return 1

    print(f"OK  round-trip for every T in [0, {total}) ({total} values)")
    print(f"OK  dial_hour in 1..12 for all 24 hours")
    if random_n:
        print(f"OK  {random_n} random instants round-trip")
    print(f"OK  worked example: {format_stamp(decompose_ms(WORKED_EXAMPLE))}")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--days", type=int, default=2,
                   help="how many days to sweep exhaustively (default: 2)")
    p.add_argument("--random", type=int, default=200_000,
                   help="number of random instants to check (default: 200000)")
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args(argv)
    return run(args.days, args.random, args.quiet)


if __name__ == "__main__":
    raise SystemExit(main())
