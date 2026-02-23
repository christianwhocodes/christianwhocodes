"""Core enumeration types."""

from enum import IntEnum, StrEnum

__all__: list[str] = ["ExitCode", "InitAction"]


class ExitCode(IntEnum):
    """Standard exit codes for CLI applications.

    Attributes:
        SUCCESS: Operation completed successfully (0).
        ERROR: Operation failed with an error (1).

    """

    SUCCESS = 0
    ERROR = 1


class InitAction(StrEnum):
    """Common initialization action names.

    Attributes:
        STARTPROJECT: The 'startproject' command/action.
        INIT: The 'init' command/action.
        CREATE: The 'create' command/action.
        NEW: The 'new' command/action.
        SETUP: The 'setup' command/action.
        BOOTSTRAP: The 'bootstrap' command/action.
        SCAFFOLD: The 'scaffold' command/action.

    """

    STARTPROJECT = "startproject"
    INIT = "init"
    CREATE = "create"
    NEW = "new"
    SETUP = "setup"
    BOOTSTRAP = "bootstrap"
    SCAFFOLD = "scaffold"
