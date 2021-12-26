from math_function import math_function
import pytest


@pytest.mark.parametrize("test_input, expected",
                         [# first range: -x^2 , [-10, -2]
                          (-10, -100),
                          (-5, -25),
                          (-2, -4),
                          # second range: (1-x) / (1+x), (-2, 8), x!= -1
                          (-1.9921875, -3.015748031496063),
                          (4, -0.6),
                          (7.9921875, -0.7775847089487402),
                          # third range: abs(x-12), (8, 35]
                          (8.0078125, 3.9921875),
                          (15, 3),
                          (35, 23)])
def test_valid_values(test_input, expected):
    assert math_function(test_input) == expected


@pytest.mark.parametrize("test_input",
                         [# first range: -x^2 , [-10, -2]
                          -100,
                          -10.0078125,
                          # second range: (1-x) / (1+x), (-2, 8), x!= -1
                          -1,
                          # between second and third
                          8,
                          # third range: abs(x-12), (8, 35]
                          35.0078125,
                          135])
def test_invalid_values(test_input):
    with pytest.raises(ValueError):
        math_function(test_input)


def test_invalid_increment():
    with pytest.raises(ValueError):
        math_function(2 + 1 / 256)
