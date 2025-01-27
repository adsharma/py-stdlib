import math

from stdlib.math import cos, pow, sin, sqrt, tan


# Test cases
def test_sin():
    test_values = [0, math.pi / 6, math.pi / 4, math.pi / 3, math.pi / 2, math.pi]
    for x in test_values:
        custom_result = sin(x)
        math_result = math.sin(x)
        assert math.isclose(
            custom_result, math_result, rel_tol=1e-9
        ), f"sin({x}) failed: {custom_result} != {math_result}"
    print("All sin() tests passed!")


def test_cos():
    test_values = [0, math.pi / 6, math.pi / 4, math.pi / 3, math.pi / 2, math.pi]
    for x in test_values:
        custom_result = cos(x)
        math_result = math.cos(x)
        assert math.isclose(
            custom_result, math_result, rel_tol=1e-9
        ), f"cos({x}) failed: {custom_result} != {math_result}"
    print("All cos() tests passed!")


def test_tan():
    test_values = [0, math.pi / 6, math.pi / 4, math.pi / 3]
    for x in test_values:
        custom_result = tan(x)
        math_result = math.tan(x)
        assert math.isclose(
            custom_result, math_result, rel_tol=1e-9
        ), f"tan({x}) failed: {custom_result} != {math_result}"
    print("All tan() tests passed!")


def test_sqrt():
    test_values = [0, 1, 2, 4, 9, 16, 25]
    for x in test_values:
        custom_result = sqrt(x)
        math_result = math.sqrt(x)
        assert math.isclose(
            custom_result, math_result, rel_tol=1e-9
        ), f"sqrt({x}) failed: {custom_result} != {math_result}"
    print("All sqrt() tests passed!")


def test_pow():
    test_values = [(0, 1), (2, 3), (3, 2), (4, 0.5), (10, -1)]
    for x, y in test_values:
        custom_result = pow(x, y)
        math_result = math.pow(x, y)
        assert math.isclose(
            custom_result, math_result, rel_tol=1e-9
        ), f"pow({x}, {y}) failed: {custom_result} != {math_result}"
    print("All pow() tests passed!")
