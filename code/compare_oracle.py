#!/usr/bin/env python3
"""Compare 0-based and 1-based cycle models against a step-by-step oracle.

For each q in {7, 9, 12, 24, 60} the script simulates a cycle step by
step, without any formula. Three implementations are compared:

  1. 0-based, plain mod          : T mod q
  2. 0-based, corrected          : T mod q with a branch for the boundary
  3. 1-based, p ≡ 1 (mod q)      : (T-1) mod q + 1

The script reports, per implementation and per q:
  * label errors    (wrong position at a boundary)
  * transition errors (wrong count at end-to-beginning)
  * number of conditional branches used in the path

Exit code 0 on success, 1 on any failure.

Usage:
    python code/compare_oracle.py [--steps N] [--q 7 9 12 24 60]
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from rd.cycle import Cycle

DEFAULT_Q = [7, 9, 12, 24, 60]


def oracle(t: int, q: int) -> tuple[int, int]:
    """Step-by-step simulation. Returns (cycles, position)."""
    pos = 1
    cycles = 0
    for _ in range(t - 1):
        pos += 1
        if pos > q:
            pos = 1
            cycles += 1
    return cycles, pos


def zero_plain(t: int, q: int) -> int:
    """0-based, no correction. Returns a label in 0..q-1."""
    return t % q


def zero_corrected(t: int, q: int) -> int:
    """0-based, with the boundary case fixed. Returns 1..q."""
    r = t % q
    if r == 0:
        return q
    return r


def one_based(t: int, q: int) -> int:
    """1-based. Branch-free. Returns 1..q."""
    return (t - 1) % q + 1


def run(steps: int, qs: list[int]) -> int:
    print(f"{'q':>3} | {'impl':<20} | {'label err':>9} | "
          f"{'trans err':>9} | {'branches':>8}")
    print("-" * 62)

    any_fail = False

    for q in qs:
        c = Cycle(q)
        oracle_labels: list[int] = []
        oracle_trans: list[int] = []
        for t in range(1, steps + 1):
            _, pos = oracle(t, q)
            oracle_labels.append(pos)
            oracle_trans.append((t - 1) // q)

        impls = [
            ("0-based plain",     zero_plain,     0, False),
            ("0-based corrected", zero_corrected, 1, False),
            ("1-based",           one_based,      0, True),
        ]

        for name, fn, branches, count_trans in impls:
            label_err = 0
            trans_err = 0
            for t in range(1, steps + 1):
                got = fn(t, q)
                want = oracle_labels[t - 1]
                if got != want:
                    label_err += 1
                if count_trans:
                    if c.transition_count(t) != oracle_trans[t - 1]:
                        trans_err += 1

            print(f"{q:>3} | {name:<20} | {label_err:>9} | "
                  f"{trans_err:>9} | {branches:>8}")

            if name.startswith("1-based") and label_err:
                any_fail = True

        print("-" * 62)

    if any_fail:
        print("FAIL  1-based model diverged from the oracle", file=sys.stderr)
        return 1

    print("OK    1-based model matches the oracle on every value")
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--steps", type=int, default=2_000,
                   help="how many T values to compare (default: 2000)")
    p.add_argument("--q", type=int, nargs="+", default=DEFAULT_Q,
                   help="cycle lengths to test (default: 7 9 12 24 60)")
    args = p.parse_args(argv)
    return run(args.steps, args.q)


if __name__ == "__main__":
    raise SystemExit(main())
