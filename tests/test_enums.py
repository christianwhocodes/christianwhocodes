"""Tests for christianwhocodes.core.enums module.

Covers the ExitCode IntEnum used as return values from CLI command handlers.
SUCCESS = 0 and ERROR = 1 follow standard Unix exit code conventions.

Run just these tests::

    uv run pytest tests/test_enums.py -v
"""

from christianwhocodes.core.enums import ExitCode


class TestExitCode:
    """Tests for the ExitCode IntEnum."""

    def test_values(self) -> None:
        """SUCCESS is 0 (standard Unix success), ERROR is 1."""
        assert ExitCode.SUCCESS == 0
        assert ExitCode.ERROR == 1

    def test_is_int(self) -> None:
        """ExitCode members are ints (IntEnum), so they can be passed directly to sys.exit() without conversion."""
        assert isinstance(ExitCode.SUCCESS, int)
        assert isinstance(ExitCode.ERROR, int)
