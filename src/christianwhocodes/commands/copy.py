"""File and directory copy command."""

from argparse import Namespace

from ..core.enums import ExitCode
from ..io.filesystem import copy_path


def handle_copy_operation(args: Namespace) -> ExitCode:
    """Copy files or directories from source to destination.

    Automatically detects whether the source is a file or directory and
    performs the appropriate copy operation with progress feedback.

    Args:
        args: Parsed arguments containing:
            - source (str): Source path to copy from
            - destination (str): Destination path to copy to

    Returns:
        ExitCode.SUCCESS if copy succeeded, ExitCode.ERROR otherwise.

    Example:
        $ christianwhocodes copy -i ./src -o ./backup/src
        Directory copied successfully from ./src to ./backup/src
    """
    success = copy_path(args.source, args.destination)
    return ExitCode.SUCCESS if success else ExitCode.ERROR


__all__: list[str] = ["handle_copy_operation"]
