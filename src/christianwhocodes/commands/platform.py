"""Platform information display command."""

from argparse import Namespace

from ..core.enums import ExitCode


def handle_platform_info(args: Namespace) -> ExitCode:
    """Display platform and architecture information.

    Shows the detected operating system, CPU architecture, and combined
    platform string in a formatted output.

    Args:
        args: Parsed command-line arguments (unused for this handler).

    Returns:
        ExitCode.SUCCESS after displaying platform information.

    Example:
        Platform: windows
        Architecture: x64
        Full: windows-x64
    """
    from ..core.platform import Platform
    from ..io.console import Text, print

    platform_info = Platform()
    print(
        [
            ("Platform: ", Text.INFO),
            (platform_info.os_name, None),
        ]
    )
    print(
        [
            ("Architecture: ", Text.INFO),
            (platform_info.architecture, None),
        ]
    )
    print(
        [
            ("Full: ", Text.INFO),
            (str(platform_info), None),
        ]
    )
    return ExitCode.SUCCESS


__all__: list[str] = ["handle_platform_info"]
