"""Display Platform Information."""

from argparse import Namespace

from ...core import BaseCommand, ExitCode, Platform

__all__: list[str] = ["PlatformCommand"]


class PlatformCommand(BaseCommand):
    """Display platform OS and architecture information."""

    prog = "platform"
    help = "Display platform information"

    def handle(self, args: Namespace) -> ExitCode:  # noqa: D102
        platform = Platform()
        print(f"OS:           {platform.os_name}")
        print(f"Architecture: {platform.architecture}")
        return ExitCode.SUCCESS
