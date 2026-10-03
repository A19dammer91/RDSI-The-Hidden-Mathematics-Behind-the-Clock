# RDSI: The Hidden Mathematics Behind the Clock

**Representation, Domain Modelling and Software Implementation.**

**Two Diophantine structures, two purposes, and a Python package that implements both.**

[![CI](https://github.com/A19dammer91/the-exact-algebraic-condition-for-clock-behaviour/actions/workflows/ci.yml/badge.svg)](https://github.com/A19dammer91/the-exact-algebraic-condition-for-clock-behaviour/actions/workflows/ci.yml)
[![branchless core](https://img.shields.io/badge/branchless%20core-enforced-success)](#the-branchless-claim)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-lightgrey)](LICENSE)

📘 **[RDSI: Representation, Domain Modelling and Software Implementation](https://doi.org/10.5281/zenodo.23077746)**
📄 **[The Clock [3600,60,1] and the (25,12)-System: A Structural Comparison](https://doi.org/10.5281/zenodo.22804148)**
🧮 **[The 19-9 System: N = 19A + 9B](https://zenodo.org/records/19474707)**
🔗 **[Interactive demo](https://a19dammer91.github.io/the-exact-algebraic-condition-for-clock-behaviour/)**
🧪 **[Companion: D³ Pattern](https://github.com/A19dammer91/D3-by-A-C-Coupling-Demo)**

---

## Start here: one question

A stopwatch has been running for **45,296,789 milliseconds**. What does the display say?

Anyone who has used a stopwatch knows the answer without thinking:

> **12:34:56.789**

But almost nobody can explain **how** you get there. Why 12 and not 11? Why does a clock jump back after 59 seconds, and not after 60 or 100?

This repository answers that question. It ships three things:

1. **Three papers** that together analyse the clock, compare it to a plain Diophantine system, and generalise the underlying pattern.
2. **A Python package** (`rd`, *Representation Domain*) that implements the cycle algebra, the Diophantine ladder, and the clock cascade.
3. **An interactive demo** where you can drag five layers and watch them carry.

---

## The everyday example: money

Imagine notes of **€25 and €12**. Pay exactly **€575**. How many ways are there?

Two:

- 11 × €25 + 25 × €12
- 23 × €25 + 0 × €12

No others. That is a **linear Diophantine equation**:

> N = 25·A + 12·B

The reason two answers exist comes from a single relation:

> **25 ≡ 1 (mod 12)**

Because of that relation, the smallest €25 count is one step: `A₀ = N mod 12`. Every other solution is reached by stepping `+12` in `A` and `−25` in `B`. That ordered family is called the **ladder**.

The smallest representable number is **264 = 24 · 11**. The largest number that cannot be represented at all is **263**. From 264 onward, every integer has at least one representation.

The RDSI paper uses `N = 500` as its worked example. There, `ladder(500, 25, 12)` gives `(8, 25)` and `(20, 0)`.

At the other extreme stands the clock.

---

## The clock uses a different Diophantine structure

Same equation shape, entirely different behaviour:

> T = 3600·H + 60·M + S

But the clock gives **exactly one** answer, not a ladder. Two reasons:

**1. Hierarchical divisibility.** Every base is an exact multiple of the next:

> 1000 ms → 1 s → 60 s → 1 min → 60 min → 1 h → 24 h → 1 day

**2. Bounded coefficients.** Seconds and minutes stay `< 60`, hours stay `< 24`.

Remove either property, and uniqueness collapses.

### Side by side

| | (25, 12) system | Clock `[3600, 60, 1]` |
|---|---|---|
| Type | Linear Diophantine | Linear Diophantine |
| Base relation | One foundation relation: `25 ≡ 1 (mod 12)` | Each base divides the next |
| Coefficient bounds | none | `< 60`, `< 60`, `< 24` |
| Number of solutions | multiple, ordered as a ladder | exactly one |
| Frobenius number | **263** | none: every instant is representable |
| Source of structure | A single residue relation | A hierarchical divisibility chain |
| Purpose | explore multiplicity | guarantee uniqueness |

A clock is not a weaker Diophantine system. It is a different one, built on purpose.

The RDSI paper proves that the modular condition `p ≡ 1 (mod q)` and positional divisibility are **structurally incompatible**. The clock does not fail to be Diophantine; it is designed not to be.

---

## The representational choice: 0-based or 1-based

This is the core insight of the RDSI paper.

Almost every cycle in software today is modelled 0-based: positions run from 0 up to and including `q − 1`. That looks neutral, but it causes a structural problem: the value that marks the **end** of the cycle is at the same time the value of the **beginning**. Midnight is both the end of the day and the start of the next. Developers know the consequences as off-by-one errors.

The RDSI paper shows that the choice between `p ≡ 0 (mod q)` and `p ≡ 1 (mod q)` is not an arithmetic choice, it is a **representational** one. The arithmetic stays identical. The model changes.

| Number T | Model 0 to 11 | Model 1 to 12 |
|---|---|---|
| 12 | position 0, called "beginning" | position 12, the end of the cycle |
| 13 | position 1 | position 1, after one transition |
| 24 | position 0: end and beginning at once | position 12: end only |
| 25 | position 1 | position 1, after two complete cycles |

With `p ≡ 1 (mod q)`, the transition from one cycle to the next becomes the **formal heart** of the model, not a by-product of the division. The number 0 never occurs as a position. There is no hour 0; that is hour 12. Hour 13 is hour 1.

### The same cycle, written two ways

| Operation | 0-based | 1-based |
|---|---|---|
| position of T | `T mod q` | `(T − 1) mod q + 1` |
| cycles elapsed | `T div q` | `(T − 1) div q` |
| transition count | `T div q` | `T div q` |

Both columns give the same arithmetic result. Only the second column keeps end and beginning separate.

---

## Why this matters

- **Time, files, coordinates.** Everywhere one big number becomes something readable (45,296,789 ms → `12:34:56.789`, 1,234,567 bytes → `1.23 MB (SI) / 1.18 MiB`, 20260917 → `17 September 2026`), the same layer structure is at work. Timestamp bugs almost always come down to these layers.
- **Teaching modulo.** Everyone understands *"11 o'clock plus 3 hours is 2 o'clock."* That is `14 mod 12 = 2`. The formula is hard; the clock is not.
- **A transferable insight.** Every layered system makes one choice: *easy to explore every combination*, or *impossible to be uncertain*. You cannot have both in one structure.

---

## The `rd` package

`rd` stands for **Representation Domain**. It implements the three representations from the papers in one small, dependency-free library.

### Install

```bash
pip install -e ".[dev]"      # editable, with test and lint tooling
```

### Use

```python
from rd.cycle    import Cycle
from rd.ladder   import ladder, frobenius, representation_count
from rd.cascade  import decompose_ms, compose_ms, format_stamp, dial_hour
from rd.adapters import to_zero_based, from_zero_based

# 1-based cycle algebra
c = Cycle(q=12, p=25)
c.position(13)            # 1     : 13 becomes 1, never 0
c.position(12)            # 12    : 12 is end, not beginning
c.cycles(25)              # 2     : two complete cycles
c.index(24)               # 0     : the smallest coefficient, may be 0

# Diophantine ladder
[(p.a, p.b) for p in ladder(500, 25, 12)]
# [(8, 25), (20, 0)]      : exactly two representations
frobenius(25, 12)         # 263   : largest non-representable N
representation_count(500, 25, 12)   # 2

# Clock cascade
s = decompose_ms(45_296_789)
format_stamp(s)           # '0 d 12:34:56.789'
compose_ms(s)             # 45_296_789  : round-trip holds
dial_hour(0)              # 12    : 0-based internally, 1-based on the dial
dial_hour(13)             # 1

# Bridge to 0-based consumers
to_zero_based(12, 12)     # 0
from_zero_based(0, 12)    # 12
```

### CLI

```bash
$ python -m rd 45296789 --ms
0 d 12:34:56.789

$ python -m rd 500 --system 25,12
R(500) = 2
  (8, 25)
  (20, 0)

$ python -m rd 263 --system 25,12
geen representatie voor N=263 in (25,12)      # Frobenius
```

---

## The branchless claim

The RDSI paper shows that a 0-based model needs **six conditional branches** to be correct at every boundary (12, 24, 36, ...), while a 1-based model `p ≡ 1 (mod q)` needs **none**. The comparison was run for `q = 7, 9, 12, 24, 60`.

That claim is not asserted here. It is a **CI gate**. Every push runs:

```bash
pytest tests/test_branchless.py -v --no-cov
```

which parses the AST of the hot-path functions and fails if any `if`, ternary, or `and`/`or` appears:

| Function | File | Branches in path |
|---|---|---|
| `Cycle.index` | `cycle.py` | 0 |
| `Cycle.position` | `cycle.py` | 0 |
| `Cycle.cycles` | `cycle.py` | 0 |
| `Cycle.decompose` | `cycle.py` | 0 |
| `Cycle.transition_count` | `cycle.py` | 0 |
| `dial_hour` | `cascade.py` | 0 |
| `to_zero_based` | `adapters.py` | 0 |
| `from_zero_based` | `adapters.py` | 0 |

Guards (`raise` in `__post_init__`, system validation in `ladder.py`) are excluded: they run at the edge, not in the path.

If someone later tries to fix a corner case by adding an `if` in `Cycle.position`, the build turns red.

---

## The four invariants

The RDSI paper records four hard properties that can be checked directly as tests:

| Property | What is checked |
|---|---|
| Foundation | For every N from 264 onward, the smallest A equals `N mod 12` |
| Ladder holds | Every pair on the ladder satisfies `25A + 12B = N` and `B >= 0` |
| Clock uniqueness | Decomposing after composing returns the original value |
| Transition | After position 12 comes position 1 with one extra cycle; position 0 never occurs |

All four pass in the reference implementation, for the ranges the paper describes.

---

## Repository structure

```
.
├── RDSI.pdf                     # Representation, Domain Modelling and Software Implementation
├── Clock_Structure.pdf          # The Clock [3600,60,1] and the (25,12)-System
├── README.md                    # this file
├── pyproject.toml               # PEP 621 metadata, hatchling build
├── .github/workflows/
│   └── ci.yml                   # test, lint, type, branchless gate
├── src/rd/
│   ├── cycle.py                 # 1-based cycle algebra
│   ├── ladder.py                # Diophantine ladder and Frobenius number
│   ├── cascade.py               # clock decomposition and display layer
│   ├── adapters.py              # 0-based to 1-based bridge
│   └── __main__.py              # CLI
├── tests/
│   ├── test_foundation.py       # A0 = N mod 12 for all N >= 264
│   ├── test_ladder.py           # every pair satisfies 25A + 12B = N
│   ├── test_cascade.py          # round-trip uniqueness
│   ├── test_transition.py       # position never 0
│   └── test_branchless.py       # AST branch counter
├── code/                        # standalone verification scripts
├── figures/                     # figures used in the papers
└── docs/                        # interactive HTML demo
```

---

## Running locally

```bash
git clone https://github.com/A19dammer91/the-exact-algebraic-condition-for-clock-behaviour
cd the-exact-algebraic-condition-for-clock-behaviour

# Linux / macOS
python -m venv .venv && source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1

pip install -e ".[dev]"

pytest                                        # full suite
pytest -m "not slow"                          # fast feedback
ruff check src tests && mypy                  # lint and types
pytest tests/test_branchless.py -v --no-cov   # the gate
```

---

## The most beautiful time a clock can show

> **12:34:56.789**

Digits 1 through 9, in order. A lucky hit of the decimal system and the 24-hour division.

In the [interactive demo](https://a19dammer91.github.io/the-exact-algebraic-condition-for-clock-behaviour/) there is a slider that **ends exactly on that time**: 45,296,789 milliseconds. Drag it all the way right and land on 12 hours, 34 minutes, 56 seconds, and 789 thousandths.

It is not a mathematical necessity. It is a tribute to the structure.

---

## Papers

This repository accompanies four Zenodo records.

| Paper | Role | DOI |
|---|---|---|
| RDSI: Representation, Domain Modelling and Software Implementation | The index paper. Introduces the representational choice `p ≡ 1 (mod q)`, the ladder, and the software implementation. | [10.5281/zenodo.23077746](https://doi.org/10.5281/zenodo.23077746) |
| The Clock [3600,60,1] and the (25,12)-System: A Structural Comparison | Structural comparison. Proves that positional divisibility and the modular condition are incompatible by design. | [10.5281/zenodo.22804148](https://doi.org/10.5281/zenodo.22804148) |
| The 19-9 System: N = 19A + 9B | Companion Diophantine structure. Same core relation, smaller coefficients. | [10.5281/zenodo.19474707](https://zenodo.org/records/19474707) |
| The D³ Pattern: Deterministic Data Decomposition by A-C Coupling | Companion pattern paper. A single anchor value and a closed rule across five layers. | [10.5281/zenodo.20819940](https://doi.org/10.5281/zenodo.20819940) |

The **19-9 system** shares the same core, `p ≡ 1 (mod q)`, with the (25,12) system. Scaling from (19,9) to (25,12) moves the Frobenius number from 143 to 263 and the structural period `pq` from 171 to 300. The anchor family, the first run of `q` consecutive representable integers, starts at 144 and 264 respectively and grows from 9 to 12 integers.

---

## Citation

```bibtex
@misc{elissaoui2026rdsi,
  title     = {Representation, Domain Modelling and Software Implementation},
  author    = {El Issaoui, Bilal},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.23077746},
  url       = {https://doi.org/10.5281/zenodo.23077746}
}

@misc{elissaoui2026clock,
  title     = {The Clock [3600,60,1] and the (25,12)-System: A Structural Comparison},
  author    = {El Issaoui, Bilal},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.22804148},
  url       = {https://doi.org/10.5281/zenodo.22804148}
}

@misc{elissaoui2026nineteen,
  title     = {The 19-9 System: N = 19A + 9B},
  author    = {El Issaoui, Bilal},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.19474707},
  url       = {https://zenodo.org/records/19474707}
}
```

---

## License

Released under **Creative Commons Attribution-NonCommercial-ShareAlike 4.0** (CC BY-NC-SA 4.0).
Commercial use is not covered by this license.

---

## Contact

**Bilal El Issaoui**, Independent Researcher, Amsterdam
elissa.oui.amster@gmail.com · elissa.oui@outlook.com

Or open an [issue](https://github.com/A19dammer91/the-exact-algebraic-condition-for-clock-behaviour/issues) or start a [discussion](https://github.com/A19dammer91/the-exact-algebraic-condition-for-clock-behaviour/discussions).
