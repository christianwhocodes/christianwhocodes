"""Mathematical utility functions for common calculations."""

import math
from typing import Generator


def is_prime(n: int) -> bool:
    """Check if a number is prime.

    A prime number is a natural number greater than 1 that has no positive
    divisors other than 1 and itself.

    Args:
        n: The number to check.

    Returns:
        True if the number is prime, False otherwise.

    Example:
        >>> is_prime(7)
        True
        >>> is_prime(10)
        False
        >>> is_prime(2)
        True
        >>> is_prime(1)
        False
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # Check odd divisors up to sqrt(n)
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def factorial(n: int) -> int:
    """Calculate the factorial of a non-negative integer.

    The factorial of n (denoted n!) is the product of all positive integers
    less than or equal to n. By convention, 0! = 1.

    Args:
        n: Non-negative integer.

    Returns:
        The factorial of n.

    Raises:
        ValueError: If n is negative.

    Example:
        >>> factorial(5)
        120
        >>> factorial(0)
        1
        >>> factorial(10)
        3628800
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    return math.factorial(n)


def is_factorial(n: int) -> bool:
    """Check if a number is a factorial of some integer.

    A factorial number is the product of all positive integers less than or
    equal to a given positive integer. For example, 120 is a factorial (5!)
    because 5! = 5 x 4 x 3 x 2 x 1 = 120.

    Args:
        n: The number to check.

    Returns:
        True if the number is a factorial, False otherwise.

    Example:
        >>> is_factorial(120)
        True
        >>> is_factorial(24)
        True
        >>> is_factorial(100)
        False
        >>> is_factorial(1)
        True
    """
    if n < 1:
        return False
    if n == 1:
        return True

    i = 2
    factorial = 1
    while factorial < n:
        factorial *= i
        i += 1

    return factorial == n


def gcd(a: int, b: int) -> int:
    """Calculate the greatest common divisor of two integers.

    Uses the Euclidean algorithm to find the largest positive integer that
    divides both numbers without a remainder.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        The greatest common divisor of a and b.

    Example:
        >>> gcd(48, 18)
        6
        >>> gcd(100, 50)
        50
        >>> gcd(17, 19)
        1
    """
    return math.gcd(a, b)


def lcm(a: int, b: int) -> int:
    """Calculate the least common multiple of two integers.

    The least common multiple is the smallest positive integer that is
    divisible by both a and b.

    Args:
        a: First integer.
        b: Second integer.

    Returns:
        The least common multiple of a and b.

    Example:
        >>> lcm(12, 18)
        36
        >>> lcm(5, 7)
        35
    """
    return math.lcm(a, b)


def fibonacci(n: int) -> int:
    """Calculate the nth Fibonacci number.

    The Fibonacci sequence is defined as:
    F(0) = 0, F(1) = 1, F(n) = F(n-1) + F(n-2) for n > 1

    Args:
        n: The position in the Fibonacci sequence (0-indexed).

    Returns:
        The nth Fibonacci number.

    Raises:
        ValueError: If n is negative.

    Example:
        >>> fibonacci(0)
        0
        >>> fibonacci(1)
        1
        >>> fibonacci(10)
        55
        >>> fibonacci(20)
        6765
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    if n <= 1:
        return n

    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    return b


def fibonacci_sequence(n: int) -> Generator[int, None, None]:
    """Generate the first n Fibonacci numbers.

    Args:
        n: Number of Fibonacci numbers to generate.

    Yields:
        Fibonacci numbers in sequence.

    Example:
        >>> list(fibonacci_sequence(7))
        [0, 1, 1, 2, 3, 5, 8]
    """
    if n <= 0:
        return

    a, b = 0, 1
    yield a
    if n == 1:
        return

    yield b
    for _ in range(2, n):
        a, b = b, a + b
        yield b


def is_perfect_square(n: int) -> bool:
    """Check if a number is a perfect square.

    A perfect square is an integer that is the square of another integer.

    Args:
        n: The number to check.

    Returns:
        True if the number is a perfect square, False otherwise.

    Example:
        >>> is_perfect_square(16)
        True
        >>> is_perfect_square(20)
        False
        >>> is_perfect_square(0)
        True
    """
    if n < 0:
        return False
    root = int(math.sqrt(n))
    return root * root == n


def is_even(n: int) -> bool:
    """Check if a number is even.

    Args:
        n: The number to check.

    Returns:
        True if the number is even, False otherwise.

    Example:
        >>> is_even(4)
        True
        >>> is_even(7)
        False
    """
    return n % 2 == 0


def is_odd(n: int) -> bool:
    """Check if a number is odd.

    Args:
        n: The number to check.

    Returns:
        True if the number is odd, False otherwise.

    Example:
        >>> is_odd(4)
        False
        >>> is_odd(7)
        True
    """
    return n % 2 != 0


def is_power_of_two(n: int) -> bool:
    """Check if a number is a power of two.

    Args:
        n: The number to check.

    Returns:
        True if the number is a power of two, False otherwise.

    Example:
        >>> is_power_of_two(8)
        True
        >>> is_power_of_two(10)
        False
        >>> is_power_of_two(1)
        True
    """
    return n > 0 and (n & (n - 1)) == 0


__all__: list[str] = [
    "is_prime",
    "is_factorial",
    "gcd",
    "lcm",
    "fibonacci",
    "fibonacci_sequence",
    "is_perfect_square",
    "factorial",
    "is_even",
    "is_odd",
    "is_power_of_two",
]
