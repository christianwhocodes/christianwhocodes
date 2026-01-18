from enum import IntEnum


class ExitCode(IntEnum):
    """Standard exit codes IntEnums.

    SUCCESS = 0
    ERROR = 1
    """

    SUCCESS = 0
    ERROR = 1


__all__: list[str] = ["ExitCode"]
