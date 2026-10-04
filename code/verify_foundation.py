#!/usr/bin/env python3
"""Verify the foundation relation A0 = N mod 12 for the (25, 12) system.

Sweep: for every N from 264 up to a configurable maximum, the smallest
coefficient A on the ladder must equal N mod 12, and 263 must have no
representation at all.

Exit code 0 on success, 1 on any failure.

Usage:
    python code/verify_foundation.py [--max N] [--quiet]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rd.ladder import frobenius, ladder

P = 25
Q = 12
FROBENIUS = 263
FIRST = 264


def run(max_n: int, quiet: bool) -> int:
    failures: list[str] = []

    if frobenius(P, Q) != FROBENIUS:
        failures.append(f"frobenius({P}, {Q}) != {FROBENIUS}")

    if ladder(FROBENIUS, P, Q):
        failures.append(f"N={FROBENIUS} should have no representation")

    checked = 0
    for n in range(FIRST, max_n + 1):
        pairs = ladder(n, P, Q)
        if not pairs:
            failures.append(f"N={n} has no representation")
            continue
        if pairs[0].a != n % Q:
            failures.append(
                f"N={n}: smallest A is {pairs[0].a}, expected {n % Q}"
            )
            continue
        checked += 1
        if not quiet and checked % 10_000 == 0:
            print(f"  ... {checked:>7} checked", file=sys.stderr)

    if failures:
        print("FAIL", file=sys.stderr)
        for line in failures[:20]:
            print(f"  {line}", file=sys.stderr)
        if len(failures) > 20:
            print(f"  ... and {len(failures) - 20} more", file=sys.stderr)
        return 1

    print(f"OK  foundation holds for every N in [{FIRST}, {max_n}] "
          f"({checked} values)")
    print(f"OK  frobenius({P}, {Q}) = {FROBENIUS}")
    print(f"OK  N = {FROBENIUS} has no representation")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--max", type=int, default=200_000,
                   help="upper bound for the sweep (default: 200000)")
    p.add_argument("--quiet", action="store_true",
                   help="suppress progress output")
    args = p.parse_args(argv)
    return run(args.max, args.quiet)


if __name__ == "__main__":
    raise SystemExit(main())
