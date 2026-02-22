"""Display Platform Information."""

from argparse import Namespace

from ...core import ExitCode, Platform, cprint

__all__: list[str] = ["handle_platform_display"]


def handle_platform_display(args: Namespace) -> ExitCode:
    """Handle the 'platform' display."""
    platform = Platform()
    cprint(f"OS:           {platform.os_name}")
    cprint(f"Architecture: {platform.architecture}")
    return ExitCode.SUCCESS
