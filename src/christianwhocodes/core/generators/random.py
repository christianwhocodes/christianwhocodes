"""Cryptographically secure random string generation."""

from string import ascii_letters, digits

__all__: list[str] = ["generate_random_string"]


def generate_random_string(
    length: int = 32,
    charset: str = ascii_letters + digits,
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
