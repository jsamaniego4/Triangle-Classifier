"""Instructor model: stained-glass customer acceptance test.

This example is AI-assisted teaching material, not a record of a student's
independent work. The three acceptance criteria are documented in README.md.
"""

from math import sqrt

from triangle import classify_triangle


def test_stained_glass_customer_orders():
    """Check buildability, shape labels, and corner reinforcement end to end."""
    # Each expected outcome is a customer requirement, supplied independently
    # of the classifier's implementation. A raised exception fails this test.
    # order, sides, expected label, buildable, needs reinforced corners
    orders = [
        ("equal-sided piece", (6, 6, 6), "Equilateral", True, False),
        ("two equal sides", (5, 5, 6), "Isosceles", True, False),
        ("three different sides", (4, 5, 6), "Scalene", True, False),
        ("zero-length side", (0, 4, 5), "Invalid", False, False),
        ("negative side", (-1, 4, 5), "Invalid", False, False),
        ("flat piece at the boundary", (2, 3, 5), "Invalid", False, False),
        ("longest side too long", (2, 3, 6), "Invalid", False, False),
        ("nonnumeric entry", ("five", 5, 6), "Invalid", False, False),
        ("right-angle piece", (3, 4, 5), "Right Scalene", True, True),
        ("right piece entered out of order", (13, 5, 12), "Right Scalene", True, True),
        ("right piece with equal legs", (5, 5, 5 * sqrt(2)), "Right Isosceles", True, True),
        ("near-right piece", (3, 4, 5.001), "Scalene", True, False),
    ]

    for order, sides, expected_label, buildable, reinforced in orders:
        result = classify_triangle(*sides)

        assert result == expected_label, f"Incorrect customer message for {order}"
        assert (result != "Invalid") == buildable, f"Incorrect buildability for {order}"
        assert result.startswith("Right ") == reinforced, f"Incorrect reinforcement flag for {order}"
