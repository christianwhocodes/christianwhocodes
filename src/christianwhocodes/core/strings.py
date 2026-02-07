"""String generation and manipulation utilities."""

import string
from typing import Any, Iterable


def generate_random_string(
    length: int = 32,
    no_clipboard: bool = False,
    charset: str = string.ascii_letters + string.digits,
) -> str:
    """Generate a cryptographically secure random string.

    Creates a random string using the secrets module for cryptographic strength
    and optionally copies it to the clipboard.

    Args:
        length: Length of the random string (default: 32).
        no_clipboard: If True, skip copying to clipboard (default: False).
        charset: Character set to use (default: alphanumeric).

    Returns:
        The generated random string.

    Example:
        >>> random_str = generate_random_string(16)
        Generated: aB3dEf7gHi9jKl2m
        Copied to clipboard!
        >>> random_str = generate_random_string(16, no_clipboard=True)
        Generated: nO5pQr8sT1uVw4xY
    """
    from secrets import choice

    from pyperclip import copy

    from ..io.console import Text, print, status

    with status("Generating secure random string..."):
        random_str = "".join(choice(charset) for _ in range(length))

    print(
        [
            ("✓ Generated: ", Text.SUCCESS),
            (random_str, Text.HIGHLIGHT),
        ]
    )

    # Copy to clipboard unless disabled
    if not no_clipboard:
        try:
            copy(random_str)
            print("✓ Copied to clipboard!", Text.SUCCESS)
        except Exception as e:
            print(f"Could not copy to clipboard: {e}", Text.WARNING, force=True)

    return random_str


def max_length_from_choices(choices: Iterable[tuple[str, Any]]) -> int:
    """Return the maximum string length from a list of choice pairs.

    Useful for formatting aligned choice lists in CLI menus.

    Args:
        choices: Iterable of (value, display) tuples.

    Returns:
        The maximum length of the value field.

    Example:
        >>> choices = [("short", "Short option"), ("very_long_option", "Long")]
        >>> max_length_from_choices(choices)
        16
    """
    return max(len(choice[0]) for choice in choices)


__all__: list[str] = ["generate_random_string", "max_length_from_choices"]
