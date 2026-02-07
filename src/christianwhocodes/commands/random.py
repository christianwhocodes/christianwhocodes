"""Random string generation command."""

from argparse import Namespace

from ..core.enums import ExitCode


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
    from ..core.strings import generate_random_string
    from ..io.console import Text, print, status

    with status("Generating secure random string..."):
        random_str = generate_random_string(length=args.length)

    print(
        [
            ("✓ Generated: ", Text.SUCCESS),
            (random_str, Text.HIGHLIGHT),
        ]
    )

    if not args.no_clipboard:
        try:
            from pyperclip import copy

            copy(random_str)
            print("✓ Copied to clipboard!", Text.SUCCESS)
        except Exception as e:
            print(f"Could not copy to clipboard: {e}", Text.WARNING, force=True)

    return ExitCode.SUCCESS


__all__: list[str] = ["handle_random_string"]
