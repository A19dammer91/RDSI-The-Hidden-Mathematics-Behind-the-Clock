"""The branchless claim as a hard CI gate.

The RDSI paper shows that a 1-based model p ≡ 1 (mod q) needs no
conditional branches in its hot path, while a 0-based model needs six
to be correct at every boundary. This test parses the AST of the
hot-path functions and fails if any branch appears.

Counted: ast.If, ast.IfExp (ternary), ast.BoolOp (and/or).
Not counted: raise-guards, i.e. an `if` whose body consists only of
`raise` statements and which has no `else`. They validate the input at
the edge (also in __post_init__ or _check_system), they are not part of
the computation in the path.
"""
from __future__ import annotations

import ast
import inspect
import textwrap
from collections.abc import Callable

import pytest

from rd.adapters import from_zero_based, to_zero_based
from rd.cascade import dial_hour
from rd.cycle import Cycle


def _is_guard(node: ast.AST) -> bool:
    """True for `if cond: raise ...` without an else branch."""
    return (
        isinstance(node, ast.If)
        and not node.orelse
        and all(isinstance(stmt, ast.Raise) for stmt in node.body)
    )


def count_branches(fn: Callable[..., object]) -> int:
    """Count conditional nodes in the function body, ignoring raise-guards."""
    tree = ast.parse(textwrap.dedent(inspect.getsource(fn)))
    branch_nodes = (ast.If, ast.IfExp, ast.BoolOp)

    guarded: set[ast.AST] = set()
    for node in ast.walk(tree):
        if _is_guard(node):
            guarded.update(ast.walk(node))

    return sum(
        isinstance(node, branch_nodes) and node not in guarded
        for node in ast.walk(tree)
    )


BRANCHLESS_CORE: list[tuple[str, Callable[..., object]]] = [
    ("Cycle.index",            Cycle.index),
    ("Cycle.position",         Cycle.position),
    ("Cycle.cycles",           Cycle.cycles),
    ("Cycle.decompose",        Cycle.decompose),
    ("Cycle.transition_count", Cycle.transition_count),
    ("dial_hour",              dial_hour),
    ("to_zero_based",          to_zero_based),
    ("from_zero_based",        from_zero_based),
]


@pytest.mark.parametrize(
    ("name", "fn"),
    BRANCHLESS_CORE,
    ids=[name for name, _ in BRANCHLESS_CORE],
)
def test_core_is_branchless(name: str, fn: Callable[..., object]) -> None:
    n = count_branches(fn)
    assert n == 0, (
        f"{name} contains {n} conditional branch(es). "
        f"The 1-based core must stay branch-free."
    )


def test_cycle_walk_is_also_branchless() -> None:
    """Cycle.walk delegates to decompose, so it inherits the property."""
    assert count_branches(Cycle.walk) == 0


def test_counter_detects_a_branch() -> None:
    """Self-check: the branch counter must find branches when present."""
    def with_if(x: int) -> int:
        if x > 0:
            return 1
        return 0

    def with_ternary(x: int) -> int:
        return 1 if x > 0 else 0

    def with_bool_op(x: int, y: int) -> bool:
        return x > 0 and y > 0

    assert count_branches(with_if) == 1
    assert count_branches(with_ternary) == 1
    assert count_branches(with_bool_op) == 1


def test_counter_ignores_raise_guards() -> None:
    """Self-check: a pure input guard is not counted as a branch."""
    def with_guard(x: int) -> int:
        if x < 1:
            raise ValueError("x >= 1 required")
        return x % 7

    def with_compound_guard(x: int, y: int) -> int:
        if x < 1 or y < 1:
            raise ValueError("x and y >= 1 required")
        return x % y

    assert count_branches(with_guard) == 0
    assert count_branches(with_compound_guard) == 0


def test_counter_still_counts_guard_lookalikes() -> None:
    """Self-check: an `if` that does more than raise is still a branch."""
    def with_else(x: int) -> int:
        if x < 1:
            raise ValueError("x >= 1 required")
        else:
            return x % 7

    def with_work_in_body(x: int) -> int:
        if x < 1:
            x = 1
            raise ValueError("x >= 1 required")
        return x % 7

    assert count_branches(with_else) == 1
    assert count_branches(with_work_in_body) == 1
    
