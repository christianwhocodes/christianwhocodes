"""String manipulation utilities."""

from typing import Any, Iterable

__all__: list[str] = ["max_length_from_choices"]


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
