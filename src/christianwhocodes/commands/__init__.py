"""CLI command handlers for all available commands.

Each module exposes a single ``handle_*`` function that receives an
``argparse.Namespace`` and returns an ``ExitCode``.  The handlers
are registered in ``cli.py``'s ``COMMAND_HANDLERS`` dict.

Modules:
    copy: handle_copy_operation — copy files/directories via Copier classes.
    generate: handle_file_generation — create config files from templates.
    platform: handle_platform_info — display OS and architecture details.
    random: handle_random_string — generate secure random strings with
            optional clipboard support.
"""

from .copy import *  # noqa: F403
from .generate import *  # noqa: F403
from .platform import *  # noqa: F403
from .random import *  # noqa: F403
