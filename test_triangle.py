"""Unit tests for triangle.py. Expected values come from the spec table, not from the code."""

import math

import pytest

from triangle import classify_triangle, is_valid_triangle


# --- Invalid: non-positive sides -------------------------------------------

@pytest.mark.parametrize("sides", [(0, 4, 5), (3, 0, 5), (3, 4, 0), (-3, 4, 5), (-1, -1, -1)])
def test_non_positive_side_is_invalid(sides):
    assert classify_triangle(*sides) == "Invalid"
    assert is_valid_triangle(*sides) is False


# --- Invalid: triangle inequality ------------------------------------------

@pytest.mark.parametrize("sides", [(1, 2, 10), (10, 1, 2), (2, 10, 1)])
def test_triangle_inequality_failure_is_invalid(sides):
    assert classify_triangle(*sides) == "Invalid"


# --- Boundary: degenerate (two sides sum exactly to the third) -------------

@pytest.mark.parametrize("sides", [(1, 2, 3), (3, 1, 2), (2, 3, 1)])
def test_degenerate_is_invalid(sides):
    assert classify_triangle(*sides) == "Invalid"
    assert is_valid_triangle(*sides) is False


def test_just_past_degenerate_is_valid():
    # A small step past the boundary still counts as a triangle.
    assert is_valid_triangle(1, 2, 2.999) is True
    assert classify_triangle(1, 2, 2.999) == "Scalene"


def test_valid_triangle_very_close_to_degenerate_boundary():
    assert is_valid_triangle(1, 2, 3 - 1e-10) is True
    assert classify_triangle(1, 2, 3 - 1e-10) == "Scalene"


def test_short_positive_side_is_not_lost_to_rounding():
    assert is_valid_triangle(1e-20, 1.0, 1.0) is True


@pytest.mark.parametrize("direction, expected", [(-math.inf, True), (math.inf, False)])
def test_immediate_neighbors_of_degenerate_boundary(direction, expected):
    assert is_valid_triangle(1.0, 2.0, math.nextafter(3.0, direction)) is expected


def test_large_integer_equilateral():
    side = 10 ** 1000
    assert classify_triangle(side, side, side) == "Equilateral"


# --- Equilateral ------------------------------------------------------------

@pytest.mark.parametrize("s", [1, 3, 7.5])
def test_equilateral(s):
    assert classify_triangle(s, s, s) == "Equilateral"


# --- Isosceles: every position of the odd side -----------------------------

@pytest.mark.parametrize("sides", [(5, 5, 3), (5, 3, 5), (3, 5, 5)])
def test_isosceles(sides):
    assert classify_triangle(*sides) == "Isosceles"


# --- Scalene ----------------------------------------------------------------

def test_scalene():
    assert classify_triangle(4, 5, 6) == "Scalene"


# --- Right triangles --------------------------------------------------------

@pytest.mark.parametrize("sides", [(3, 4, 5), (5, 3, 4), (5, 12, 13)])
def test_right_scalene_integer(sides):
    assert classify_triangle(*sides) == "Right Scalene"


def test_right_isosceles_non_integer():
    # (5 * sqrt(2))**2 is 50.00000000000001 in floats, not 50.
    # An implementation using == for the Pythagorean check returns "Isosceles".
    assert classify_triangle(5, 5, 5 * math.sqrt(2)) == "Right Isosceles"


def test_right_scalene_non_integer():
    assert classify_triangle(1, math.sqrt(3), 2) == "Right Scalene"


def test_near_right_is_not_right():
    # Tolerance must not be so loose that a clearly non-right triangle passes.
    assert classify_triangle(3, 4, 5.01) == "Scalene"


@pytest.mark.parametrize("scale", [1e-200, 1e200])
def test_right_triangle_at_different_scales(scale):
    assert classify_triangle(3 * scale, 4 * scale, 5 * scale) == "Right Scalene"


# --- Robustness -------------------------------------------------------------

@pytest.mark.parametrize("sides", [
    ("3", 4, 5), (None, 4, 5), (True, True, True),
    (float("nan"), 4, 5), (float("inf"), 4, 5),
])
def test_non_numeric_input_is_invalid_not_crash(sides):
    assert classify_triangle(*sides) == "Invalid"
