import pytest

from .fib import fib

@pytest.mark.parametrize(
    "n, expected", [
        (0,0),
        (1,1),
        (2,1),
        (3,2),
        (4,3),
        (5,5),
        (6,8),
        (10,55),
    ]
)
def test_fibonacci(n, expected):
    assert fib(n) == expected