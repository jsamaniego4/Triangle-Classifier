"""Triangle classifier.

classify_triangle(a, b, c) returns one of:
    "Invalid", "Equilateral", "Isosceles", "Scalene",
    "Right Isosceles", "Right Scalene"
"""

import math
from numbers import Real

# Relative tolerance for the Pythagorean check only.
REL_TOL = 1e-9


def _is_number(x) -> bool:
    """True for finite real numbers. bool is rejected even though it is an int subclass."""
    return isinstance(x, Real) and not isinstance(x, bool) and math.isfinite(x)


def is_valid_triangle(a, b, c) -> bool:
    """Return True if a, b, c can form a non-degenerate triangle.

    Invalid when any side is not a finite number, any side is <= 0, or the
    triangle inequality fails. Equality at the degenerate boundary is invalid.
    Side lengths are interpreted as the supplied real numeric values.
    """
    if not all(_is_number(s) for s in (a, b, c)):
        return False
    if a <= 0 or b <= 0 or c <= 0:
        return False
    x, y, z = sorted((a, b, c))  # z is the longest side
    # Only the longest side can violate the inequality.
    if x + y <= z:
        return False
    return True


def _is_right(a, b, c) -> bool:
    x, y, z = sorted((a, b, c))
    # Normalize before squaring to avoid overflow or underflow at large or
    # small scales. z is positive because validation runs first.
    return math.isclose((x / z) ** 2 + (y / z) ** 2, 1.0, rel_tol=REL_TOL)


def classify_triangle(a, b, c) -> str:
    """Classify finite real side lengths; invalid inputs return 'Invalid'."""
    if not is_valid_triangle(a, b, c):
        return "Invalid"

    if a == b == c:
        return "Equilateral"  # can never be right; see README

    if a == b or b == c or a == c:
        kind = "Isosceles"
    else:
        kind = "Scalene"

    return f"Right {kind}" if _is_right(a, b, c) else kind
