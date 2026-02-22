"""Core enumeration types."""

from enum import IntEnum


__all__: list[str] = ["ExitCode"]


class ExitCode(IntEnum):
    """Standard exit codes for CLI applications.

    Attributes:
        SUCCESS: Operation completed successfully (0).
        ERROR: Operation failed with an error (1).

    """

    SUCCESS = 0
    ERROR = 1
