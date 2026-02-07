"""Tests for christianwhocodes.core.math module.

Covers all public math utility functions: primality checks, factorials,
GCD/LCM, Fibonacci, perfect squares, parity, and power-of-two detection.

Each class tests a single function with:
- Typical correct inputs (happy path)
- Boundary values (0, 1, 2)
- Negative input validation (should raise ValueError)

Run just these tests::

    uv run pytest tests/test_math.py -v
"""

import pytest

from christianwhocodes.core.math import (
    fibonacci,
    fibonacci_sequence,
    gcd,
    is_even,
    is_factorial,
    is_odd,
    is_perfect_square,
    is_power_of_two,
    is_prime,
    lcm,
)

# ============================================================================
# is_prime — checks whether a number has no divisors other than 1 and itself
# ============================================================================


class TestIsPrime:
    """Tests for the is_prime() function."""

    def test_small_primes(self) -> None:
        """The smallest primes (2, 3, 5, 7) should all return True."""
        assert is_prime(2) is True
        assert is_prime(3) is True
        assert is_prime(5) is True
        assert is_prime(7) is True

    def test_non_primes(self) -> None:
        """0, 1, and composite numbers should return False."""
        assert is_prime(0) is False
        assert is_prime(1) is False  # 1 is not prime by convention
        assert is_prime(4) is False
        assert is_prime(9) is False
        assert is_prime(100) is False

    def test_large_prime(self) -> None:
        """7919 is the 1000th prime — verifies the sqrt-based loop works."""
        assert is_prime(7919) is True

    def test_even_composite(self) -> None:
        """Even composites are caught by the n % 2 == 0 early exit."""
        assert is_prime(10) is False
        assert is_prime(1000) is False

    def test_negative_raises(self) -> None:
        """Negative inputs are not valid and must raise ValueError."""
        with pytest.raises(ValueError, match="non-negative"):
            is_prime(-1)


# ============================================================================
# is_factorial — checks whether n equals k! for some integer k
# ============================================================================


class TestIsFactorial:
    """Tests for the is_factorial() function.

    Returns (True, k) if n == k!, or (False, None) otherwise.
    Special case: 1 is both 0! and 1! — the function returns (True, 0).
    """

    def test_known_factorials(self) -> None:
        """Verify known factorial values: 1=0!, 2=2!, 6=3!, 24=4!, etc."""
        assert is_factorial(1) == (True, 0)
        assert is_factorial(2) == (True, 2)
        assert is_factorial(6) == (True, 3)
        assert is_factorial(24) == (True, 4)
        assert is_factorial(120) == (True, 5)
        assert is_factorial(720) == (True, 6)

    def test_non_factorials(self) -> None:
        """Numbers that are not factorials should return (False, None)."""
        assert is_factorial(0) == (False, None)  # 0 is not a factorial
        assert is_factorial(5) == (False, None)
        assert is_factorial(100) == (False, None)

    def test_negative_raises(self) -> None:
        """Negative inputs must raise ValueError."""
        with pytest.raises(ValueError, match="non-negative"):
            is_factorial(-1)


# ============================================================================
# gcd / lcm — wrappers around math.gcd and math.lcm
# ============================================================================


class TestGcdLcm:
    """Tests for gcd() and lcm() functions."""

    def test_gcd_basic(self) -> None:
        """Standard GCD calculations using the Euclidean algorithm."""
        assert gcd(48, 18) == 6
        assert gcd(100, 50) == 50
        assert gcd(17, 19) == 1  # coprime numbers

    def test_gcd_with_zero(self) -> None:
        """GCD(0, n) == n by mathematical convention."""
        assert gcd(0, 5) == 5
        assert gcd(5, 0) == 5

    def test_lcm_basic(self) -> None:
        """Standard LCM calculations."""
        assert lcm(12, 18) == 36
        assert lcm(5, 7) == 35  # coprime → LCM = product

    def test_lcm_same_number(self) -> None:
        """LCM of a number with itself is the number itself."""
        assert lcm(10, 10) == 10


# ============================================================================
# fibonacci — iterative computation of the nth Fibonacci number
# ============================================================================


class TestFibonacci:
    """Tests for the fibonacci() function (0-indexed)."""

    def test_base_cases(self) -> None:
        """F(0) = 0 and F(1) = 1 by definition."""
        assert fibonacci(0) == 0
        assert fibonacci(1) == 1

    def test_known_values(self) -> None:
        """Verify well-known Fibonacci numbers."""
        assert fibonacci(10) == 55
        assert fibonacci(20) == 6765

    def test_negative_raises(self) -> None:
        """Negative indices are not valid and must raise ValueError."""
        with pytest.raises(ValueError, match="non-negative"):
            fibonacci(-1)


class TestFibonacciSequence:
    """Tests for the fibonacci_sequence() generator.

    fibonacci_sequence(n) yields the first n Fibonacci numbers: F(0)..F(n-1).
    """

    def test_first_seven(self) -> None:
        """First 7 Fibonacci numbers: 0, 1, 1, 2, 3, 5, 8."""
        assert list(fibonacci_sequence(7)) == [0, 1, 1, 2, 3, 5, 8]

    def test_zero_length(self) -> None:
        """Requesting 0 items should yield an empty sequence."""
        assert list(fibonacci_sequence(0)) == []

    def test_single_element(self) -> None:
        """Requesting 1 item should yield just [0]."""
        assert list(fibonacci_sequence(1)) == [0]

    def test_two_elements(self) -> None:
        """Requesting 2 items should yield [0, 1]."""
        assert list(fibonacci_sequence(2)) == [0, 1]

    def test_negative_raises(self) -> None:
        """Negative count must raise ValueError."""
        with pytest.raises(ValueError, match="non-negative"):
            list(fibonacci_sequence(-1))


# ============================================================================
# is_perfect_square — checks if n == k² for some integer k
# ============================================================================


class TestIsPerfectSquare:
    """Tests for the is_perfect_square() function.

    Uses math.isqrt internally for exact integer arithmetic (no float errors).
    """

    def test_perfect_squares(self) -> None:
        """Standard perfect squares should return True."""
        assert is_perfect_square(0) is True
        assert is_perfect_square(1) is True
        assert is_perfect_square(4) is True
        assert is_perfect_square(16) is True
        assert is_perfect_square(144) is True

    def test_non_perfect_squares(self) -> None:
        """Non-perfect-squares should return False."""
        assert is_perfect_square(2) is False
        assert is_perfect_square(3) is False
        assert is_perfect_square(20) is False

    def test_large_perfect_square(self) -> None:
        """Verify correctness for very large integers.

        This is the key test for the math.isqrt fix — using int(math.sqrt(n))
        would lose precision for numbers this large and give wrong results.
        """
        n = 10**18  # 1,000,000,000,000,000,000
        assert is_perfect_square(n * n) is True
        assert is_perfect_square(n * n + 1) is False

    def test_negative_raises(self) -> None:
        """Negative inputs must raise ValueError."""
        with pytest.raises(ValueError, match="non-negative"):
            is_perfect_square(-4)


# ============================================================================
# is_even / is_odd / is_power_of_two — simple parity and bit checks
# ============================================================================


class TestIsEven:
    """Tests for the is_even() function (n % 2 == 0)."""

    def test_even(self) -> None:
        """Even numbers, including 0 and negatives."""
        assert is_even(0) is True
        assert is_even(2) is True
        assert is_even(-4) is True

    def test_odd(self) -> None:
        """Odd numbers should return False."""
        assert is_even(1) is False
        assert is_even(7) is False


class TestIsOdd:
    """Tests for the is_odd() function (n % 2 != 0)."""

    def test_odd(self) -> None:
        """Odd numbers, including negatives."""
        assert is_odd(1) is True
        assert is_odd(7) is True
        assert is_odd(-3) is True

    def test_even(self) -> None:
        """Even numbers should return False."""
        assert is_odd(0) is False
        assert is_odd(2) is False


class TestIsPowerOfTwo:
    """Tests for the is_power_of_two() function.

    Uses the bit trick: n > 0 and (n & (n - 1)) == 0.
    """

    def test_powers_of_two(self) -> None:
        """Known powers of two: 1 (2⁰), 2 (2¹), 8 (2³), 1024 (2¹⁰)."""
        assert is_power_of_two(1) is True
        assert is_power_of_two(2) is True
        assert is_power_of_two(8) is True
        assert is_power_of_two(1024) is True

    def test_non_powers(self) -> None:
        """0 and non-powers should return False."""
        assert is_power_of_two(0) is False  # 0 is not a power of two
        assert is_power_of_two(3) is False
        assert is_power_of_two(10) is False

    def test_negative_raises(self) -> None:
        """Negative inputs must raise ValueError."""
        with pytest.raises(ValueError, match="non-negative"):
            is_power_of_two(-2)
