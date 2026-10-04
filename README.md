# RDSI: The Hidden Mathematics Behind the Clock

**How a huge number becomes something you can read, and why one small choice, counting from 1 instead of 0, removes a whole family of bugs.**

[![CI](https://github.com/A19dammer91/RDSI-The-Hidden-Mathematics-Behind-the-Clock/actions/workflows/ci.yml/badge.svg)](https://github.com/A19dammer91/RDSI-The-Hidden-Mathematics-Behind-the-Clock/actions/workflows/ci.yml)
[![no special cases in the core](https://img.shields.io/badge/branchless%20core-enforced-success)](#no-special-cases-needed)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)](https://www.python.org/downloads/)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-lightgrey)](https://github.com/A19dammer91/RDSI-The-Hidden-Mathematics-Behind-the-Clock/blob/main/LICENSE)

[📘 **Main paper**](https://doi.org/10.5281/zenodo.23077746) ·
[📄 **Clock paper**](https://doi.org/10.5281/zenodo.22804148) ·
[🔗 **Interactive demo**](https://a19dammer91.github.io/RDSI-The-Hidden-Mathematics-Behind-the-Clock/) ·
[📋 **How to cite**](#how-to-cite)

---

## The question

A stopwatch has been running for **45,296,789 milliseconds**. What does it show?

> **12:34:56.789**

Everyone can read a stopwatch. Almost nobody can say *how* the number turns into that display. Why does the clock wrap around after 59 seconds, and not after 60 or 100? Why is there an hour 12 but no hour 0?

This project answers those questions with simple examples, working code and checks you can run yourself. It contains:

- **Papers** that explain the clock and compare it with a different kind of number puzzle
- **A small Python library** (`rd`) with no extra dependencies
- **An interactive demo** where you drag a slider and watch the units carry over

## Quick start

```bash
git clone https://github.com/A19dammer91/RDSI-The-Hidden-Mathematics-Behind-the-Clock
cd RDSI-The-Hidden-Mathematics-Behind-the-Clock
pip install -e ".[dev]"

python -m rd 45296789 --ms
# 0 d 12:34:56.789
```

You need Python 3.10 or newer.

---

## The core idea

The fundamental idea is simple: **shifting from 0-based to 1-based counting removes the need for complicated software workarounds.**

In a cycle of length `q` (for a 12-hour dial, `q = 12`):

- `T = q` is the **end** of a cycle.
- `T = q + 1` is the **start** of the next one.

Because of that, two short formulas are enough. They are the heart of the library:

```text
Cycle.position(T)  =  ((T - 1) % q) + 1     which step of the cycle you are on (1 to q)
Cycle.cycles(T)    =   (T - 1) // q         how many full cycles lie behind you
```

Here `%` is the remainder of a division and `//` is the whole-number part. For `q = 12`:

| T | `position` | `cycles` | What it means |
|---|---|---|---|
| 1 | 1 | 0 | first step of the first cycle |
| 11 | 11 | 0 | |
| 12 | 12 | 0 | **end** of the first cycle |
| 13 | 1 | 1 | **start** of the second cycle |
| 24 | 12 | 1 | end of the second cycle |
| 25 | 1 | 2 | start of the third cycle |

These formulas express the cycle entirely through arithmetic. Instead of bit tricks or extra `if` checks at the boundaries, the structure comes straight from the algebra. No logical jumps are needed by design, which removes a common source of off-by-one errors and keeps the execution path clean and predictable. A test enforces this on every push (see [No special cases needed](#no-special-cases-needed)).

### How the layers chain together

`Cycle.cycles(T)` returns a clean whole number: how many full cycles lie behind you, with no leftovers and no special values. Because of that, the result can be handed straight to the next layer of a larger system, for example from seconds to minutes, or from hours to a day counter, without any clean-up in between. Each layer uses the same kind of arithmetic as the one before it. This chain of layers is the **cascade**.

The stopwatch from the question is built this way. Each layer shows its remainder and passes the whole number on:

| Layer | Input | Shown (remainder) | Passed on (whole number) |
|---|---|---|---|
| milliseconds → seconds | 45,296,789 ms | 789 ms | 45,296 s |
| seconds → minutes | 45,296 s | 56 s | 754 min |
| minutes → hours | 754 min | 34 min | 12 h |
| hours → days | 12 h | 12 h | 0 days |

Result: 0 days, 12:34:56.789. Adding a new layer, such as weeks or years, means adding one more row, not a new rule.

One detail: inside the stopwatch, elapsed time starts at 0 (00:00:00 is a real moment), so the whole numbers can be passed on as they are. The 1-based rule applies at the **dial**, where a cycle must show its end: hour 0 is displayed as 12. Count something from 1 and you add 1 when you hand the number to the next layer.

### Why counting from 0 causes trouble

Most software counts positions from 0: for a 12-hour dial, positions 0 to 11. That looks harmless, but **the end of one cycle and the start of the next get the same number.** Midnight is both the end of one day and the start of the next. Programmers know the result as the "off-by-one error".

Counting 1 to 12 keeps the end and the start apart:

| Number | Counting 0 to 11 | Counting 1 to 12 |
|---|---|---|
| 12 | position 0, which is "the beginning" | position 12, the end of the cycle |
| 13 | position 1 | position 1, after one full cycle |
| 24 | position 0, end and beginning at once | position 12, the end only |
| 25 | position 1 | position 1, after two full cycles |

This is why a clock face has no hour 0: after 12 comes 1. The same calculation, written both ways:

| | Counting from 0 | Counting from 1 |
|---|---|---|
| Position of number T | `T % q` | `((T - 1) % q) + 1` |
| Full cycles behind T | `T // q` | `(T - 1) // q` |

---

## Example 1: the stopwatch

Take 45,296,789 milliseconds and peel off one unit at a time:

| Step | Calculation | Result |
|---|---|---|
| Whole hours | 45,296,789 ÷ 3,600,000 | **12** hours, remainder 2,096,789 |
| Whole minutes | 2,096,789 ÷ 60,000 | **34** minutes, remainder 56,789 |
| Whole seconds | 56,789 ÷ 1,000 | **56** seconds, remainder 789 |
| Left over | | **789** milliseconds |

Result: **12:34:56.789**. Running it backwards (12 h + 34 min + 56 s + 789 ms) gives exactly 45,296,789 again.

The important part: **there is only one right answer.** No other combination of hours, minutes and seconds gives the same total, as long as minutes and seconds stay below 60 and hours below 24.

## Example 2: paying with €25 and €12 notes

Now a different puzzle. You have notes of **€25** and **€12**, and you want to pay exactly **€575**. How many ways are there?

Exactly two:

- 11 notes of €25 and 25 notes of €12
- 23 notes of €25 and no notes of €12

Unlike the clock, this puzzle has **several** answers. It behaves neatly because 25 is exactly one more than 2 × 12, so 25 ≡ 1 (mod 12). Because of that single fact:

- The smallest number of €25 notes you need is simply **the remainder of the amount divided by 12**. For €575 that is 575 ÷ 12 = 47 remainder 11, so **11 notes**.
- Every other way to pay is found by adding 12 more €25 notes and giving back 25 of the €12 notes. In the library this list of all possible ways is called the **ladder**.

Two more facts worth knowing:

- **263** is the largest amount you can never pay with these notes.
- From **264** onwards, every amount can be paid in at least one way.

A smaller one to try by hand: for €500 the two ways are 8 × €25 + 25 × €12, and 20 × €25 + 0 × €12.

---

## Why the clock has one answer and the notes have several

Both puzzles have the same shape (add up multiples of some numbers), but they are built for opposite goals.

| | €25 / €12 notes | Clock (hours, minutes, seconds) |
|---|---|---|
| Goal | explore every possible combination | guarantee exactly one answer |
| Why it works | 25 is one more than a multiple of 12 | every unit divides evenly into the next |
| Limits on each unit | none | seconds and minutes below 60, hours below 24 |
| Number of answers | several (the ladder) | exactly one |
| Amounts that cannot be made | up to 263 | none, every moment can be shown |

A clock is not a weaker version of the notes puzzle. It is a different design with a different goal. The Clock paper shows that you cannot have both properties in the same system.

## Why this matters

- **Dates and times.** Whenever a large number becomes something readable, the same layered structure is at work: 45,296,789 ms → `12:34:56.789`, 1,234,567 bytes → `1.23 MB`, 20260917 → `17 September 2026`. Many timestamp bugs come from getting one of these layers wrong.
- **Teaching.** Everyone understands that 3 hours after 11 o'clock is 2 o'clock. That is the remainder rule (14 mod 12 = 2), and the clock makes it obvious.
- **A general lesson.** A layered system can be built to *explore all combinations* or to *leave no room for doubt*. It cannot do both at once.

---

## Using the library

```python
from rd.cycle    import Cycle
from rd.ladder   import ladder, frobenius, representation_count
from rd.cascade  import decompose_ms, compose_ms, format_stamp, dial_hour
from rd.adapters import to_zero_based, from_zero_based

# A 12-step cycle counted from 1
c = Cycle(q=12, p=25)
c.position(13)            # 1  : 13 wraps round to 1, never to 0
c.position(12)            # 12 : 12 is the end of the cycle
c.cycles(25)              # 2  : two full cycles completed

# All ways to pay 500 with 25s and 12s
[(p.a, p.b) for p in ladder(500, 25, 12)]
# [(8, 25), (20, 0)]      : exactly two ways
representation_count(500, 25, 12)   # 2
frobenius(25, 12)                   # 263 : the largest amount that cannot be paid

# The stopwatch
s = decompose_ms(45_296_789)
format_stamp(s)           # '0 d 12:34:56.789'
compose_ms(s)             # 45296789 : going back gives the original number
dial_hour(0)              # 12 : midnight is shown as 12
dial_hour(13)             # 1  : 1 p.m. is shown as 1

# Converting between "from 1" and "from 0" for other software
to_zero_based(12, 12)     # 0
from_zero_based(0, 12)    # 12
```

### Command line

```bash
$ python -m rd 45296789 --ms
0 d 12:34:56.789

$ python -m rd 500 --system 25,12
R(500) = 2
  (8, 25)
  (20, 0)

$ python -m rd 263 --system 25,12
no representation for N=263 in (25,12)
```

The last example is the largest amount that cannot be paid, so there is no answer.

---

## No special cases needed

The main paper claims that when you count from 1, the core calculation needs **no special cases at all**. When you count from 0, you need six extra "if this is a boundary, do something different" rules to be correct at every boundary (12, 24, 36 and so on). The comparison was run for cycle lengths 7, 9, 12, 24 and 60.

This claim is **enforced automatically**. Every time code is pushed, a test reads the source code of the core functions and fails if it finds any `if`, any `x if y else z`, or any `and`/`or`:

```bash
pytest tests/test_branchless.py -v --no-cov
```

| Function | File | Special cases |
|---|---|---|
| `Cycle.index` | `cycle.py` | 0 |
| `Cycle.position` | `cycle.py` | 0 |
| `Cycle.cycles` | `cycle.py` | 0 |
| `Cycle.decompose` | `cycle.py` | 0 |
| `Cycle.transition_count` | `cycle.py` | 0 |
| `decompose_ms` | `cascade.py` | 0 |
| `compose_ms` | `cascade.py` | 0 |
| `dial_hour` | `cascade.py` | 0 |
| `to_zero_based` | `adapters.py` | 0 |
| `from_zero_based` | `adapters.py` | 0 |

One exception is allowed: an input check that only rejects bad values by raising an error (for example "the cycle length must be at least 1"). It does not take part in the calculation, so it is not counted. Any other `if` added to the core makes the build fail.

---

## How it is checked

### Four properties

The main paper states four properties. Each one is a test:

| Property | In plain words |
|---|---|
| **Smallest-number rule** | For every amount from 264 upwards, the smallest number of €25 notes equals the amount's remainder when divided by 12. |
| **Every way adds up** | Every combination in the ladder really adds up to the amount, with no negative counts. |
| **Clock round trip** | Splitting a number into days, hours, minutes and seconds and putting it back together gives the original number. |
| **The wrap-around** | After position 12 comes position 1 and one more completed cycle. Position 0 never appears. |

All four pass for the ranges described in the paper.

### Standalone scripts

The `code/` folder holds four scripts that re-check these properties. They run straight from the project folder, without installing anything. Each one ends with exit code 0 when everything passes and 1 when something fails.

| Script | What it checks | Default range |
|---|---|---|
| `verify_foundation.py` | The smallest-number rule, and that 263 cannot be paid | 264 to 200,000 |
| `verify_ladder.py` | Every combination adds up, a fast count matches a slow one-by-one count, and the steps are always +12 and −25 | 0 to 5,000 |
| `verify_clock.py` | The clock round trip, the limits of each unit, the dial always showing 1 to 12, and the 12:34:56.789 example | 2 days and 200,000 random moments |
| `compare_oracle.py` | Counting from 1 against a slow step-by-step simulation, for cycle lengths 7, 9, 12, 24 and 60 | 2,000 steps each |

```bash
python code/verify_foundation.py --max 200000
python code/verify_ladder.py --max 5000
python code/verify_clock.py --days 2 --random 200000
python code/compare_oracle.py --steps 2000
```

Add `--quiet` to hide the progress output, or `--help` to see all options.

### What the comparison shows

`compare_oracle.py` produces the numbers behind the "no special cases" claim. For a 12-step cycle:

| Method | Wrong results | Special cases needed |
|---|---|---|
| Counting from 0, plain | at every boundary (12, 24, 36, ...) | 0 |
| Counting from 0, corrected | none | 6 |
| Counting from 1 | none | 0 |

---

## The most beautiful time a clock can show

> **12:34:56.789**

The digits 1 to 9 in order, a lucky meeting of the decimal system and the 24-hour day.

In the [interactive demo](https://a19dammer91.github.io/RDSI-The-Hidden-Mathematics-Behind-the-Clock/) there is a slider that ends exactly on that moment: 45,296,789 milliseconds. Drag it all the way to the right. It is not a mathematical necessity, just a small tribute to the structure.

---

## Project layout

```
.
├── papers/
│   ├── RDSI.pdf                 # Main paper
│   └── Clock_Structure.pdf      # The clock and the (25,12)-system
├── src/rd/                      # The Python library
│   ├── __init__.py              # What the library offers
│   ├── __main__.py              # The command line tool
│   ├── cycle.py                 # Cycles counted from 1
│   ├── ladder.py                # All ways to pay an amount, and the largest amount that cannot be paid
│   ├── cascade.py               # Splitting a number into days, hours, minutes, seconds
│   └── adapters.py              # Converting between counting from 1 and from 0
├── tests/                       # Automatic tests
│   ├── test_foundation.py
│   ├── test_ladder.py
│   ├── test_cascade.py
│   ├── test_transition.py
│   ├── test_adapters.py
│   ├── test_cli.py
│   ├── test_exports.py
│   └── test_branchless.py       # The "no special cases" check
├── code/                        # Standalone verification scripts
│   ├── verify_foundation.py
│   ├── verify_ladder.py
│   ├── verify_clock.py
│   └── compare_oracle.py
├── docs/
│   └── index.html               # The interactive demo (published with GitHub Pages)
├── .github/workflows/ci.yml     # Runs all checks on every push
├── CITATION.cff                 # How to cite this work
├── LICENSE                      # CC BY-NC-SA 4.0
├── pyproject.toml               # Package settings
└── README.md                    # This file
```

## Development

```bash
python -m venv .venv
source .venv/bin/activate         # Windows (PowerShell): .venv\Scripts\Activate.ps1
pip install -e ".[dev]"

pytest                            # all tests (takes a few minutes)
pytest -m "not slow"              # quick tests only
ruff check src tests code         # style check
ruff format --check src tests code  # formatting check
mypy src                          # type check
```

---

## Papers

The first two are also included as PDFs in the [`papers/`](https://github.com/A19dammer91/RDSI-The-Hidden-Mathematics-Behind-the-Clock/tree/main/papers) folder.

| Paper | What it covers | DOI |
|---|---|---|
| RDSI: Representation, Domain Modelling and Software Implementation | The main paper. Counting from 1, the ladder, and the software. | [10.5281/zenodo.23077746](https://doi.org/10.5281/zenodo.23077746) |
| The Clock [3600,60,1] and the (25,12)-System: A Structural Comparison | Why a clock has one answer and the notes puzzle has several, and why one system cannot have both. | [10.5281/zenodo.22804148](https://doi.org/10.5281/zenodo.22804148) |
| The 19-9 System: N = 19A + 9B | A second example of the same idea with smaller numbers (19 and 9). | [10.5281/zenodo.19474707](https://zenodo.org/records/19474707) |

The 19-9 system follows the same rule as the 25-12 system. Going from (19, 9) to (25, 12) moves the largest amount that cannot be paid from 143 to 263. The first run of consecutive payable amounts starts at 144 and 264, and its length grows from 9 to 12.

**Related work:** [The D³ Pattern](https://doi.org/10.5281/zenodo.20819940) is a separate project that applies a similar layered idea elsewhere.

---

## How to cite

GitHub's **Cite this repository** button (right-hand side of this page) uses `CITATION.cff`. For BibTeX:

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

## License

Released under **Creative Commons Attribution-NonCommercial-ShareAlike 4.0** (CC BY-NC-SA 4.0). Commercial use is not covered by this license.

## Contact

**Bilal El Issaoui**, Independent Researcher, Amsterdam
elissa.oui.amster@gmail.com · elissa.oui@outlook.com

Or open an [issue](https://github.com/A19dammer91/RDSI-The-Hidden-Mathematics-Behind-the-Clock/issues) or start a [discussion](https://github.com/A19dammer91/RDSI-The-Hidden-Mathematics-Behind-the-Clock/discussions).
