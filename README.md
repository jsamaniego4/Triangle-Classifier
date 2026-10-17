# Triangle Classifier

This project checks whether three side lengths make a triangle, identifies its
shape, and flags right triangles. It includes unit tests and a stained-glass
customer acceptance test.

Repo: [Triangle-Classifier](https://github.com/jsamaniego4/Triangle-Classifier)

## Running the tests

You need Python 3.9 or newer. From the project folder on Windows:

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

To run just one test file, add `test_triangle.py` or `test_acceptance.py`
after `pytest` in the command.

The last run passed **38 tests**: 37 unit-test cases and one acceptance test.
The acceptance test checks 12 customer orders. Parameterized inputs each count
as a separate pytest case.

## How it works

`is_valid_triangle(a, b, c)` returns `True` or `False`.
`classify_triangle(a, b, c)` returns these exact labels:

| Side lengths | Result |
| --- | --- |
| Any side is zero or negative, or two sides add up to less than or equal to the third | `Invalid` |
| All three sides equal | `Equilateral` |
| Exactly two sides equal | `Isosceles` |
| All sides different | `Scalene` |
| Right triangle with two equal sides | `Right Isosceles` |
| Right triangle with different sides | `Right Scalene` |

The code checks validity first and sorts the sides so their order does not
matter. Text, missing values, booleans, NaN, and infinity also return `Invalid`.

For equal positive sides s, the Pythagorean theorem would require
2*s*s = s*s, which only works if s = 0. A zero-length side is invalid, so an
equilateral triangle cannot also be right.

## Equivalence classes and boundaries

| Case | Inputs | Expected result |
| --- | --- | --- |
| Zero side | (0, 4, 5), with the zero in each position | `Invalid` |
| Negative side | (-3, 4, 5) | `Invalid` |
| Failed triangle inequality | (1, 2, 10), in different orders | `Invalid` |
| Degenerate triangle | (1, 2, 3), in different orders | `Invalid` |
| Just inside the valid boundary | (1, 2, 3 - 1e-10) | `Scalene` |
| Closest float on each side of the boundary | (1, 2, math.nextafter(3, direction)), toward negative or positive infinity | Valid below 3; invalid above 3 |
| All sides equal | (3, 3, 3) | `Equilateral` |
| Exactly two sides equal | (5, 5, 3), in different orders | `Isosceles` |
| All sides different | (4, 5, 6) | `Scalene` |
| Integer right triangle | (3, 4, 5), in different orders | `Right Scalene` |
| Non-integer right isosceles | (5, 5, 5*sqrt(2)) | `Right Isosceles` |
| Non-integer right scalene | (1, sqrt(3), 2) | `Right Scalene` |
| Near right, outside tolerance | (3, 4, 5.01) | `Scalene` |
| Very small or large sides | (3k, 4k, 5k), k = 1e-200 or 1e200 | `Right Scalene` |
| Very short positive side | (1e-20, 1, 1) | Valid |
| Large equal integers | Three sides of 10**1000 | `Equilateral` |
| Bad input | Text, None, bool, NaN, infinity | `Invalid` |

The two main boundaries are a side length of zero and two sides adding up
exactly to the third. The triangle inequality stays strict, without a tolerance.
For sorted sides, the code checks `x > z - y`, which avoids losing a very small
positive side when adding floats. Float inputs use their stored binary values.

The right-angle check uses `math.isclose` with relative tolerance `1e-9` and
zero absolute tolerance. It divides the sides by the longest side before
squaring, which avoids overflow and underflow. Side equality follows the
specification's exact comparisons. Comparing the returned strings with `==`
is fine; the tolerance is for the numeric Pythagorean check.

## Copilot Review Log

Copilot was used for the original drafts. This log records the checks and
changes made while reviewing the files, rather than quoting autocomplete text
that was not saved.

| Test | Copilot-suggested? | Kept / edited / rejected | Why |
| --- | --- | --- | --- |
| `test_non_positive_side_is_invalid` | Yes, original draft | Kept | Covers zero and negative sides, including different positions for zero. The table says any side <= 0 is invalid. |
| `test_degenerate_is_invalid` | Yes, original draft | Edited | Used exact integer boundary cases. Removed the decimal case because binary float rounding makes it a different boundary check. |
| `test_equilateral` | Yes, original draft | Kept | Positive equal sides must return `Equilateral`, without a right-angle prefix. |
| `test_isosceles` | Yes, original draft | Kept | Checks each position of the unequal side instead of assuming it is always last. |
| `test_scalene` | Yes, original draft | Kept | (4, 5, 6) is valid, has three different sides, and is not right. |
| `test_right_isosceles_non_integer` | Yes, original draft | Kept | (5, 5, 5*sqrt(2)) must return `Right Isosceles`. This catches a numeric Pythagorean check that incorrectly uses `==`. |
| `test_valid_triangle_very_close_to_degenerate_boundary` | No, added during Codex review | Edited | Caught a real mistake: the old validation used `math.isclose` at the triangle-inequality boundary and rejected (1, 2, 3 - 1e-10). That triangle is valid under the specification, so validation was fixed and the test was added. |
| `test_large_integer_equilateral` | No, added during Codex review | Edited | Caught an overflow in the original finite-number check for large integers. Integer validation was corrected and the test was added. |

Expected labels come from the assignment table, not from whatever the code
happens to return.

## Three ways I steered Copilot

1. **Started with the requirements.** "Write pytest tests from this table. Cover
   invalid, equilateral, isosceles, scalene, and right triangles. Explain which
   requirement each test checks so I can review the expected result."
2. **Asked about rounding.** "Include legs 5 and 5 with hypotenuse 5*sqrt(2), and
   include a near-right triangle that should not get the right-angle prefix.
   Explain where math.isclose is needed and where == is correct."
3. **Push on the boundaries.** "Check values just below, equal to, and above the
   degenerate boundary. Try the longest side in different positions. Let me
   review each suggestion, and leave the acceptance criteria and acceptance
   test for me to write independently."

## Acceptance criteria

The stained-glass studio needs the shape, a clear result for unbuildable
pieces, and a flag for corners that need reinforcement.

1. **Correct shape:** For (6, 6, 6), (5, 5, 6), and (4, 5, 6), return exactly
   `Equilateral`, `Isosceles`, and `Scalene`. Every buildable order in the
   test must match its expected label.
2. **Invalid input without a crash:** The zero, negative, degenerate, impossible,
   and non-numeric orders in the test must each return exactly `Invalid`,
   with no exceptions.
3. **Right-angle flag:** (3, 4, 5), (13, 5, 12), and (5, 5, 5*sqrt(2)) must
   return the correct shape with the `Right ` prefix. Ordinary triangles and
   the near-right order (3, 4, 5.001) must not get that prefix. No missed or
   incorrect flags are allowed in the test.

`test_acceptance.py` has one end-to-end test with 12 orders. It calls
`classify_triangle()` directly and checks the full label, whether the piece is
buildable, and whether it needs reinforced corners. An exception fails the test.
The expected results are listed separately from the implementation.

## AI-use disclosure

- **GitHub Copilot:** Used for the original implementation and unit-test drafts.
- **OpenAI Codex:** Helped review and fix the code, add tests, write the acceptance
  criteria and acceptance test, and revise this README.
- **Verification:** Expected labels were checked against the assignment table.
  Both test files passed: 38 cases total. `git diff --check` also passed.

## Submission

The repo includes `triangle.py`, `test_triangle.py`, `test_acceptance.py`,
`requirements.txt`, and this README. Use `git log --oneline` to see the
implementation, testing, and documentation commits.

Repo URL: https://github.com/jsamaniego4/Triangle-Classifier
