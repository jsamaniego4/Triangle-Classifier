# Triangle Classifier

Instructor model assignment with working code, unit tests, and one customer
acceptance test. The Copilot review log and student disclosure are illustrative
examples, not a transcript of an observed Copilot session. Students must write
their own acceptance criteria and acceptance test without Copilot.

Repository: [jsamaniego4/Triangle-Classifier](https://github.com/jsamaniego4/Triangle-Classifier)

## Run the tests

Requires Python 3.9 or newer. On Windows, from this directory:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -v
```

On macOS or Linux:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python -m pytest -v
```

Use the environment's Python with `-m pytest test_triangle.py -v` to run unit
tests, or `-m pytest test_acceptance.py -v` to run the single acceptance test.
Parameterized inputs each appear as separate pytest cases.

Verified result: **38 passed** (37 unit-test cases and one acceptance test).
Both project copies were checked with `py -m pytest -q -p no:cacheprovider`;
disabling pytest's optional cache avoids local cache permission warnings.

## Required behavior

`is_valid_triangle(a, b, c)` returns a boolean.
`classify_triangle(a, b, c)` returns the exact strings below:

| Condition | Result |
| --- | --- |
| Any side <= 0, or triangle inequality fails, including equality | `Invalid` |
| All sides equal | `Equilateral` |
| Exactly two sides equal | `Isosceles` |
| All sides different | `Scalene` |
| Right triangle, exactly two sides equal | `Right Isosceles` |
| Right triangle, all sides different | `Right Scalene` |

Invalid input is handled first. Side order does not affect classification.
Text, None, bool, NaN, and infinity also return `Invalid` as extra input handling.

For positive equal sides s, the Pythagorean equation requires 2*s*s = s*s,
which implies s = 0. Zero-length sides are invalid, so an equilateral triangle
can never be right.

## Equivalence classes and boundaries

| Class or boundary | Representative inputs | Expected result | Unit test |
| --- | --- | --- | --- |
| Zero or negative side | (0, 4, 5), (-3, 4, 5) | `Invalid` | `test_non_positive_side_is_invalid` |
| Inequality failure | (1, 2, 10), reordered | `Invalid` | `test_triangle_inequality_failure_is_invalid` |
| Degenerate equality | (1, 2, 3), reordered | `Invalid` | `test_degenerate_is_invalid` |
| Just inside valid boundary | (1, 2, 3 - 1e-10) | `Scalene` | `test_valid_triangle_very_close_to_degenerate_boundary` |
| Closest floats below/above degeneracy | (1, 2, nextafter(3, -inf / +inf)) | Valid / invalid | `test_immediate_neighbors_of_degenerate_boundary` |
| All equal | (3, 3, 3) | `Equilateral` | `test_equilateral` |
| Exactly two equal | (5, 5, 3), reordered | `Isosceles` | `test_isosceles` |
| All different | (4, 5, 6) | `Scalene` | `test_scalene` |
| Integer right | (3, 4, 5), reordered | `Right Scalene` | `test_right_scalene_integer` |
| Non-integer right isosceles | (5, 5, 5*sqrt(2)) | `Right Isosceles` | `test_right_isosceles_non_integer` |
| Non-integer right scalene | (1, sqrt(3), 2) | `Right Scalene` | `test_right_scalene_non_integer` |
| Near-right outside tolerance | (3, 4, 5.01) | `Scalene` | `test_near_right_is_not_right` |
| Extreme float scales | (3k, 4k, 5k), k=1e-200 or 1e200 | `Right Scalene` | `test_right_triangle_at_different_scales` |
| Very short positive side | (1e-20, 1, 1) | Valid | `test_short_positive_side_is_not_lost_to_rounding` |
| Large equal integers | (10**1000, 10**1000, 10**1000) | `Equilateral` | `test_large_integer_equilateral` |
| Malformed or non-finite values | text, None, bool, NaN, infinity | `Invalid` | `test_non_numeric_input_is_invalid_not_crash` |

For sorted sides x <= y <= z, validation requires `x > z - y`. This is strict
triangle inequality, with no tolerance at the degenerate boundary. Float inputs
are interpreted as their stored binary values, not exact decimal quantities.

Right-angle detection uses `math.isclose((x/z)**2 + (y/z)**2, 1.0,
rel_tol=1e-9)` with zero absolute tolerance. Normalization avoids overflow and
underflow when squaring side lengths. Side equality follows the specification's
exact equality; only the Pythagorean check uses a tolerance. Expected result
strings are correctly compared using `==`.

## Copilot Review Log

**Illustrative instructor example:** Students should record their actual
suggestions and decisions with this level of detail. These sample events are
not a claim about a real autocomplete session.

| Test | Copilot-suggested? | Kept / edited / rejected | Why |
| --- | --- | --- | --- |
| `test_non_positive_side_is_invalid` | Yes (example) | Edited | Expanded a zero-only suggestion to include negatives and different side positions; every side <= 0 is invalid. |
| `test_degenerate_is_invalid` | Yes (example) | Rejected, then replaced | Suggested `Scalene` for (1, 2, 3). Corrected to `Invalid`: 1 + 2 = 3 is degenerate. |
| `test_equilateral` | Yes (example) | Kept | Positive equal sides require `Equilateral`, never a `Right ` prefix. |
| `test_isosceles` | Yes (example) | Edited | Added all positions of the unequal side to detect order-dependent code. |
| `test_scalene` | Yes (example) | Kept | (4, 5, 6) has three different sides, satisfies strict inequality, and is not right. |
| `test_right_scalene_integer` | Yes (example) | Edited | Corrected `Scalene` to `Right Scalene` for (3, 4, 5); the right-angle prefix is required. |
| `test_right_isosceles_non_integer` | Yes (example) | Edited | Replaced an integer-only suggestion with (5, 5, 5*sqrt(2)), which catches numeric Pythagorean equality using `==`. Kept exact string assertion `== "Right Isosceles"`. |
| `test_near_right_is_not_right` | Yes (example) | Kept | (3, 4, 5.01) must not receive a false reinforcement flag. |

Review expected values against the specification rather than current program
output. Do not copy the classifier's internal logic to calculate expected labels.

## Three ways I would steer Copilot

These example prompts demonstrate student direction and review:

1. **Use the specification as the source of truth.** "Draft pytest tests from
   this table, covering invalid, equilateral, isosceles, scalene, and right
   triangles. Derive expected results from the requirements, not triangle.py.
   Identify the requirement each suggestion checks so I can review it."
2. **Challenge floating-point comparisons.** "Include legs 5 and 5 with
   hypotenuse 5*sqrt(2), plus a near-right negative case. Explain why the numeric
   Pythagorean comparison needs math.isclose, while expected strings use ==."
3. **Probe boundaries and side ordering.** "Suggest cases below, equal to, and
   above the degenerate boundary, and move the longest or unequal side into
   different positions. Let me accept, edit, or reject each test against the
   table. Leave acceptance criteria and the acceptance test for me to write
   independently without AI assistance."

## Acceptance criteria: stained-glass studio

The reference order sheet in `test_acceptance.py` makes the customer's needs
measurable:

1. **AC1 - Buildable shape labels:** (6, 6, 6), (5, 5, 6), and (4, 5, 6)
   return exactly `Equilateral`, `Isosceles`, and `Scalene`. Every buildable
   reference order returns its specified shape label rather than `Invalid`.
2. **AC2 - Unbuildable orders:** Every reference order with zero, negative,
   degenerate, impossible, or non-numeric sides returns exactly `Invalid`, with
   zero exceptions. This is the invalid-input message at the function boundary.
3. **AC3 - Reinforcement flags:** (3, 4, 5), (13, 5, 12), and
   (5, 5, 5*sqrt(2)) return the expected `Right `-prefixed shape labels. Ordinary
   orders and near-right (3, 4, 5.001) have no `Right ` prefix. Pass threshold:
   zero missed or false reinforcement flags across the reference order sheet.

One acceptance test calls `classify_triangle()` end-to-end for all 12 orders,
checking exact messages, buildability, and reinforcement. Exceptions fail the
test automatically. Expected outcomes are independently specified rather than
computed from implementation helpers. Passing these examples establishes the
reference cases, not a proof for every possible input.

## AI-use disclosure

**Example student disclosure for the modeled Copilot workflow:**

- **Tool:** GitHub Copilot autocomplete.
- **Use:** Drafting implementation and unit-test suggestions, each reviewed
  against the assignment table. The review log illustrates kept, edited, and
  rejected suggestions and specific mistakes a student should catch.
- **Verification:** Review labels against the specification, check degeneracy
  and floating-point tolerance, then run the unit and acceptance tests.
- **Acceptance work:** For a student submission, the student writes acceptance
  criteria and the acceptance test independently, without Copilot.

**Instructor example preparation:** OpenAI Codex helped assemble, review, and
test this reference implementation, unit tests, acceptance example, and README.
The student disclosure and Copilot review entries above model the requested
workflow; they are not records of an observed Copilot session.

## Submission

Required files: `triangle.py`, `test_triangle.py`, `test_acceptance.py`,
`requirements.txt`, and `README.md`. Inspect `git log --oneline` for the history
of meaningful implementation, testing, and documentation commits.

Submission URL: https://github.com/jsamaniego4/Triangle-Classifier
