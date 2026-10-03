#!/usr/bin/env python3
"""Verify the ladder for N = p*A + q*B with p ≡ 1 (mod q).

For every N up to a configurable maximum:
  * every pair returned by ladder() satisfies p*A + q*B = N and B >= 0
  * the fast counter agrees with a brute-force enumeration
  * the pairs are ordered by increasing A and decreasing B
  * consecutive pairs differ by exactly +q in A and -p in B

Exit code 0 on success, 1 on any failure.

Usage:
    python code/verify_ladder.py [--max N] [--p P] [--q Q]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rd.ladder import ladder, representation_count  # noqa: E402


def brute_force_count(n: int, p: int, q: int) -> int:
    if n < 0:
        return 0
    total = 0
    a = 0
    while p * a <= n:
        if (n - p * a) % q == 0:
            total += 1
        a += 1
    return total


def run(max_n: int, p: int, q: int, quiet: bool) -> int:
    if (p - 1) % q != 0:
        print(f"FAIL  {p} is not ≡ 1 (mod {q})", file=sys.stderr)
        return 1

    failures: list[str] = []
    checked = 0

    for n in range(0, max_n + 1):
        pairs = ladder(n, p, q)

        for pair in pairs:
            if pair.value(p, q) != n:
                failures.append(
                    f"N={n}: p*A + q*B = {pair.value(p, q)}, expected {n}"
                )
            if pair.b < 0:
                failures.append(f"N={n}: negative B = {pair.b}")
            if pair.a < 0:
                failures.append(f"N={n}: negative A = {pair.a}")

        for left, right in zip(pairs, pairs[1:]):
            if right.a - left.a != q:
                failures.append(f"N={n}: step in A is {right.a - left.a}, "
                                f"expected {q}")
            if left.b - right.b != p:
                failures.append(f"N={n}: step in B is {left.b - right.b}, "
                                f"expected {p}")

        fast = representation_count(n, p, q)
        slow = brute_force_count(n, p, q)
        if fast != slow:
            failures.append(f"N={n}: count {fast} != brute force {slow}")

        checked += 1
        if not quiet and checked % 1_000 == 0:
            print(f"  ... {checked:>6} checked", file=sys.stderr)

    if failures:
        print("FAIL", file=sys.stderr)
        for line in failures[:20]:
            print(f"  {line}", file=sys.stderr)
        if len(failures) > 20:
            print(f"  ... and {len(failures) - 20} more", file=sys.stderr)
        return 1

    print(f"OK  ladder holds for every N in [0, {max_n}] in ({p}, {q})")
    print(f"OK  fast count matches brute force on all {checked} values")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--max", type=int, default=5_000,
                   help="upper bound for the sweep (default: 5000)")
    p.add_argument("--p", type=int, default=25)
    p.add_argument("--q", type=int, default=12)
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args(argv)
    return run(args.max, args.p, args.q, args.quiet)


if __name__ == "__main__":
    raise SystemExit(main())
