"""Representation Domain (RD).

1-based cycle algebra, Diophantine ladder, and clock cascade.

Three domains, one representation choice: p ≡ 1 (mod q).
"""

from rd.adapters import from_zero_based, to_zero_based
from rd.cascade import Stamp, compose_ms, decompose_ms, dial_hour, format_stamp
from rd.cycle import Cycle, Decomposition
from rd.ladder import Pair, frobenius, ladder, representation_count

__version__ = "1.0.0"

__all__ = [
    "Cycle",
    "Decomposition",
    "Pair",
    "Stamp",
    "compose_ms",
    "decompose_ms",
    "dial_hour",
    "format_stamp",
    "frobenius",
    "from_zero_based",
    "ladder",
    "representation_count",
    "to_zero_based",
]
