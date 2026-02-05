"""Christian Who Codes CLI - Command-line interface entry point.

This module provides the main entry point for the CLI tool, including
argument parser configuration and command routing. Command implementations
are organized in the commands/ package for maintainability.
"""

from argparse import ArgumentParser, Namespace
from sys import argv, exit
from typing import Any, Callable, NoReturn

from christianwhocodes.commands import (
    handle_copy_operation,
    handle_file_generation,
    handle_platform_info,
    handle_random_string,
)
from christianwhocodes.core import ExitCode, Version
from christianwhocodes.generators import FileGeneratorOption
from christianwhocodes.io import Text, print

# ============================================================================
# ARGUMENT PARSER CONFIGURATION
# ============================================================================


def configure_random_parser(subparsers: Any) -> None:
    """Configure the random string generation subcommand.

    Args:
        subparsers: The subparsers action object to add the random parser to.
    """
    random_parser = subparsers.add_parser(
        "random",
        aliases=["generaterandom", "randomstring"],
        help="Generate a cryptographically secure random string",
    )
    random_parser.add_argument(
        "--no-clipboard",
        action="store_true",
        help="Don't copy the generated string to clipboard",
    )
    random_parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=16,
        metavar="N",
        help="Length of the random string (default: 16)",
    )


def configure_generate_parser(subparsers: Any) -> None:
    """Configure the file generation subcommand.

    Args:
        subparsers: The subparsers action object to add the generate parser to.
    """
    file_types = ", ".join(opt.value for opt in FileGeneratorOption)
    generate_parser = subparsers.add_parser(
        "generate",
        help=f"Generate configuration files ({file_types})",
    )
    generate_parser.add_argument(
        "-f",
        "--file",
        choices=[opt.value for opt in FileGeneratorOption],
        required=True,
        type=FileGeneratorOption,
        metavar="TYPE",
        help=f"File type to generate. Options: {file_types}",
    )
    generate_parser.add_argument(
        "--force",
        action="store_true",
        help="Force overwrite existing files without confirmation",
    )


def configure_copy_parser(subparsers: Any) -> None:
    """Configure the copy operation subcommand.

    Args:
        subparsers: The subparsers action object to add the copy parser to.
    """
    copy_parser = subparsers.add_parser(
        "copy",
        help="Copy files or directories from source to destination",
    )
    copy_parser.add_argument(
        "-i",
        "--input",
        "--source",
        dest="source",
        required=True,
        metavar="PATH",
        help="Source file or directory path",
    )
    copy_parser.add_argument(
        "-o",
        "--output",
        "--destination",
        dest="destination",
        required=True,
        metavar="PATH",
        help="Destination file or directory path",
    )


def create_parser() -> ArgumentParser:
    """Create and configure the argument parser with all subcommands.

    Returns:
        Configured argument parser ready to parse arguments.
    """
    parser = ArgumentParser(
        prog="christianwhocodes",
        description="Christian Who Codes CLI Tool - Utilities for developers",
        epilog="...but the people who know their God shall be strong, and carry out great exploits. — Daniel 11:32",
    )

    # Global arguments
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=Version.get("christianwhocodes")[0],
        help="Show program version and exit",
    )

    parser.add_argument(
        "-p",
        "--platform",
        action="store_true",
        help="Display platform and architecture information",
    )

    # Create subparsers for commands
    subparsers = parser.add_subparsers(
        dest="command",
        help="Available commands (use <command> -h for command-specific help)",
    )

    # Configure each subcommand
    configure_random_parser(subparsers)
    configure_generate_parser(subparsers)
    configure_copy_parser(subparsers)

    return parser


# ============================================================================
# COMMAND ROUTING AND EXECUTION
# ============================================================================

# Command registry maps command names to their handler functions
COMMAND_HANDLERS: dict[str, Callable[[Namespace], ExitCode]] = {
    "random": handle_random_string,
    "generaterandom": handle_random_string,
    "randomstring": handle_random_string,
    "generate": handle_file_generation,
    "copy": handle_copy_operation,
}


def handle_default(args: Namespace) -> ExitCode:
    """Display default message when no command is specified.

    Args:
        args: Parsed command-line arguments (unused).

    Returns:
        ExitCode.SUCCESS after displaying the message.
    """
    print(
        "...but the people who know their God shall be strong, and carry out great exploits. [purple]—[/] [bold green]Daniel[/] 11:32"
    )
    return ExitCode.SUCCESS


def dispatch_command(args: Namespace) -> ExitCode:
    """Route the command to its appropriate handler function.

    Args:
        args: Parsed command-line arguments containing the command name.

    Returns:
        ExitCode from the command handler, or default handler if no command.
    """
    # Handle platform flag (takes precedence over subcommands)
    if args.platform:
        return handle_platform_info(args)

    # Dispatch to registered command handler or default
    command = args.command
    handler = COMMAND_HANDLERS.get(command, handle_default)
    return handler(args)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================


def main() -> NoReturn:
    """Main entry point for the CLI application.

    Parses command-line arguments, dispatches to the appropriate handler,
    and exits with the returned exit code.

    This function never returns normally; it always calls sys.exit().
    """
    parser = create_parser()
    args = parser.parse_args(argv[1:])

    try:
        exit_code = dispatch_command(args)
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nOperation cancelled by user.", Text.WARNING)
        exit_code = ExitCode.ERROR
    except Exception as e:
        # Catch unexpected errors and provide debugging information
        print(f"Error: {e}", Text.ERROR)
        exit_code = ExitCode.ERROR

    exit(exit_code)


if __name__ == "__main__":
    main()
