"""Core enumeration types."""

from enum import IntEnum, StrEnum

from .platform import Platform

__all__: list[str] = ["ExitCode", "InitAction", "PostgresFilename"]


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


class PostgresFilename(StrEnum):
    """Standard PostgreSQL-related filenames.

    Attributes:
        PGPASS: The password file name; uses `pgpass.conf` on Windows and
            `.pgpass` on other platforms.
        PGSERVICE: The service configuration file name, `.pg_service.conf`.

    """

    PGPASS = "pgpass.conf" if Platform().os_name == "windows" else ".pgpass"
    PGSERVICE = ".pg_service.conf"
