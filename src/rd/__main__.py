"""CLI for the Representation Domain package.

Usage:
    python -m rd 45296789 --ms
    python -m rd 500 --system 25,12
"""

from __future__ import annotations

import argparse
import sys

from rd.cascade import decompose_ms, format_stamp
from rd.ladder import ladder


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="rd",
        description="Representation Domain: cycles, ladders, cascades.",
    )
    p.add_argument("n", type=int, help="the value N or timestamp T")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument(
        "--ms",
        action="store_true",
        help="decompose N as milliseconds since midnight",
    )
    g.add_argument(
        "--system",
        metavar="P,Q",
        help="generate the ladder for the (P,Q) system",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    if args.ms:
        print(format_stamp(decompose_ms(args.n)))
        return 0

    try:
        p_str, q_str = args.system.split(",", 1)
        p, q = int(p_str), int(q_str)
    except ValueError:
        print("--system verwacht de vorm P,Q (bv. 25,12)", file=sys.stderr)
        return 2

    try:
        pairs = ladder(args.n, p, q)
    except ValueError as exc:
        print(f"ongeldig systeem: {exc}", file=sys.stderr)
        return 2

    if not pairs:
        print(f"geen representatie voor N={args.n} in ({p},{q})")
        return 1

    print(f"R({args.n}) = {len(pairs)}")
    for pair in pairs:
        print(f"  ({pair.a}, {pair.b})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
