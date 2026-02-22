"""String generation and manipulation utilities."""

import string
from typing import Any, Iterable


def generate_random_string(
    length: int = 32,
    charset: str = string.ascii_letters + string.digits,
) -> str:
    """Generate a cryptographically secure random string.

    Uses the secrets module for cryptographic strength. This is a pure function
    with no side effects — clipboard and console output are handled by the CLI layer.

    Args:
        length: Length of the random string (default: 32).
        charset: Character set to use (default: alphanumeric).

    Returns:
        The generated random string.

    Raises:
        ValueError: If length is not positive.

    Example:
        >>> generate_random_string(16)
        'aB3dEf7gHi9jKl2m'

    """
    if length <= 0:
        raise ValueError("length must be positive")

    from secrets import choice

    return "".join(choice(charset) for _ in range(length))


def max_length_from_choices(choices: Iterable[tuple[str, Any]]) -> int:
    """Return the maximum string length from a list of choice pairs.

    Useful for formatting aligned choice lists in CLI menus.

    Args:
        choices: Iterable of (value, display) tuples.

    Returns:
        The maximum length of the value field, or 0 if choices is empty.

    Example:
        >>> choices = [("short", "Short option"), ("very_long_option", "Long")]
        >>> max_length_from_choices(choices)
        16
        >>> max_length_from_choices([])
        0

    """
    return max((len(choice[0]) for choice in choices), default=0)


__all__: list[str] = ["generate_random_string", "max_length_from_choices"]
