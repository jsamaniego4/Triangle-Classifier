# Triangle Classifier

Classifies numeric side lengths as `Invalid`, `Equilateral`, `Isosceles`,
`Scalene`, `Right Isosceles`, or `Right Scalene`.

## Run tests

Install Python 3, then run these commands from this directory:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -v
```

`test_acceptance.py` is currently a placeholder and collects no tests.

## Why equilateral triangles cannot be right

For positive equal sides s, the Pythagorean equation would require
2*s*s = s*s, which implies s = 0. Zero-length sides are invalid.

## Equivalence classes and boundaries

| Class | Example | Expected result |
| --- | --- | --- |
| Zero or negative side | (0, 4, 5), (-3, 4, 5) | Invalid |
| Triangle inequality fails | (1, 2, 10) and reordered sides | Invalid |
| Degenerate boundary | (1, 2, 3) and reordered sides | Invalid |
| Just inside valid boundary | (1, 2, 3 - 1e-10) | Scalene |
| Three equal sides | (3, 3, 3) | Equilateral |
| Exactly two equal sides | (5, 5, 3) and reordered sides | Isosceles |
| Three different sides | (4, 5, 6) | Scalene |
| Integer right triangle | (3, 4, 5) | Right Scalene |
| Non-integer right triangle | (5, 5, 5*sqrt(2)) | Right Isosceles |
| Near right but outside tolerance | (3, 4, 5.01) | Scalene |
| Non-numeric or non-finite values (additional behavior) | None, text, NaN, infinity, bool | Invalid |

Validation uses strict triangle inequality. Floating-point inputs use their
stored numeric values; no tolerance is applied to the buildability boundary.
Right-angle detection uses `math.isclose` with relative tolerance `1e-9` on
squared side ratios normalized by the longest side, avoiding square overflow.
Exact equality is appropriate for comparing the returned classification strings.

## Copilot Review Log — student must complete

The current unit tests are AI-assisted reference drafts, not Copilot evidence.
Use Copilot autocomplete to draft your tests, review each suggestion against the
assignment, and record what actually happened. Include a specific mistake you
caught; do not claim a hypothetical suggestion was produced by Copilot.

| Test | Copilot-suggested? | Kept / edited / rejected | Why |
| --- | --- | --- | --- |
| To be completed from your actual Copilot session | | | |

Check that non-integer right triangles pass and degenerate triangles fail.
A numeric Pythagorean comparison using `==` can miss irrational right triangles;
the expected string comparison in a test should still use `==`.

## Acceptance criteria — student must write

Write your own 2–3 measurable criteria from the customer's requirements and
implement one end-to-end test in `test_acceptance.py`. This section is intentionally
unfinished because the assignment reserves this judgment for you.

## AI-use disclosure

- The pre-existing Downloads project disclosed Claude authorship of its code,
  unit tests, acceptance test, criteria, and README.
- OpenAI Codex reused the implementation and unit-test drafts, corrected strict
  boundary validation, normalized right-angle arithmetic, added regression tests,
  and wrote this README and the acceptance-file placeholder.
- The prior AI-written acceptance criteria and acceptance test were not reused.
- GitHub Copilot use: not yet recorded; complete after your own session.
- Verification: Codex ran `py -m pytest -q`: 33 unit-test cases passed.
  Pytest reported a cache-directory permission warning; no acceptance test is
  implemented or verified yet. `git diff --check` also passed.

## Submission checklist

- Finish the genuine Copilot review log and Copilot-drafted unit tests.
- Write your own acceptance criteria and one acceptance test.
- Run pytest and record the result.
- Make at least three meaningful commits, for example implementation, reviewed
  unit tests, and your acceptance test plus documentation.
- Publish a public GitHub repository and submit its URL.
