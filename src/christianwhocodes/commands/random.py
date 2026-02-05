"""Random string generation command."""

from argparse import Namespace

from ..core.enums import ExitCode
from ..core.strings import generate_random_string


def handle_random_string(args: Namespace) -> ExitCode:
    """Generate a cryptographically secure random string.

    Creates a random string of the specified length and optionally copies
    it to the clipboard for easy pasting.

    Args:
        args: Parsed arguments containing:
            - length (int): Desired string length
            - no_clipboard (bool): Whether to skip clipboard copy

    Returns:
        ExitCode.SUCCESS after generating and optionally copying the string.

    Example:
        $ christianwhocodes random -l 16
        Generated: aB3dEf7gHi9jKl2m
        Copied to clipboard!
    """
    generate_random_string(length=args.length, no_clipboard=args.no_clipboard)
    return ExitCode.SUCCESS


__all__: list[str] = ["handle_random_string"]
