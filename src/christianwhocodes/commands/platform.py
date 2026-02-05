"""Platform information display command."""

from argparse import Namespace

from ..core.enums import ExitCode
from ..core.platform import PlatformInfo
from ..io.console import print


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
    platform_info = PlatformInfo()
    print(f"[bold cyan]Platform:[/] {platform_info.os_name}")
    print(f"[bold cyan]Architecture:[/] {platform_info.architecture}")
    print(f"[bold cyan]Full:[/] {platform_info}")
    return ExitCode.SUCCESS


__all__: list[str] = ["handle_platform_info"]
