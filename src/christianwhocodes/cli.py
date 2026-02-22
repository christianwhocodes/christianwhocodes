"""CLI entry point for the christianwhocodes package."""

from argparse import ArgumentParser, Namespace
from sys import exit

from christianwhocodes.commands import handle_copy_operation, handle_random_string
from christianwhocodes.core import ExitCode, Text, Version, cprint


def handle_default(args: Namespace) -> ExitCode:
    """Handle default command when no subcommand is specified."""
    cprint("...but the people who know their God shall be strong... — Daniel 11:32")
    return ExitCode.SUCCESS


def main() -> None:
    """Parse command-line arguments and execute the appropriate handler."""
    parser = ArgumentParser(prog="christianwhocodes", description="Dev Utilities")

    # 1. Global Metadata
    parser.add_argument(
        "-v", "--version", action="version", version=Version.get("christianwhocodes")[0]
    )
    parser.set_defaults(func=handle_default)  # Default if no subcommand

    subparsers = parser.add_subparsers(dest="command")

    # 2. Random String Command
    rand = subparsers.add_parser(
        "random",
        aliases=["rand", "randomstring"],
        help="Random string generator",
    )
    rand.add_argument(
        "-l",
        "--length",
        type=int,
        default=16,
    )
    rand.add_argument(
        "--no-clipboard",
        dest="no_clipboard",
        action="store_true",
        default=False,
        help="Skip copying to clipboard",
    )
    rand.set_defaults(func=handle_random_string)  # Link handler directly

    # 3. Copy Command
    copy = subparsers.add_parser("copy", help="Copy files/dirs")
    copy.add_argument("-i", "--input", "--source", dest="source", required=True)
    copy.add_argument("-o", "--output", "--destination", dest="destination", required=True)
    copy.set_defaults(func=handle_copy_operation)  # Link handler directly

    # --- Execution Logic ---
    args = parser.parse_args()

    try:
        # No dictionary needed. Just call the function attached to the args.
        exit_code = args.func(args)
    except KeyboardInterrupt:
        cprint("\nOperation cancelled.", Text.WARNING, force=True)
        exit_code = ExitCode.ERROR
    except Exception as e:
        cprint(f"Error: {e}", Text.ERROR, force=True)
        exit_code = ExitCode.ERROR

    exit(exit_code)


if __name__ == "__main__":
    main()
