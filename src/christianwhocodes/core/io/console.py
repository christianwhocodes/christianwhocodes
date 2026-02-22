"""Console output utilities for rich-formatted text."""

from contextlib import contextmanager
from enum import StrEnum
from typing import Generator

from rich.console import Console
from rich.markup import escape
from rich.theme import Theme

__all__: list[str] = [
    "Text",
    "cprint",
    "status",
]


class Text(StrEnum):
    """Semantic color codes for styled console output.

    Attributes:
        ERROR: Bold red styling for error messages.
        WARNING: Bold yellow styling for warning messages.
        SUCCESS: Bold green styling for success messages.
        INFO: Bold cyan styling for informational messages.
        DEBUG: Bold magenta styling for debug messages.
        HIGHLIGHT: Bold blue styling for highlighted text.

    """

    ERROR = "error"
    WARNING = "warning"
    SUCCESS = "success"
    INFO = "info"
    DEBUG = "debug"
    HIGHLIGHT = "highlight"


# Configure rich console with custom theme
_THEME = Theme(
    {
        Text.ERROR: "bold red",
        Text.WARNING: "bold yellow",
        Text.SUCCESS: "bold green",
        Text.INFO: "bold cyan",
        Text.DEBUG: "bold magenta",
        Text.HIGHLIGHT: "bold blue",
    }
)

_console = Console(theme=_THEME)


def cprint(
    text: str | list[tuple[str, str | None]],
    color: str | None = None,
    end: str = "\n",
) -> None:
    """Print colored text to the console using rich formatting.

    Supports both single-color and multi-color output modes for flexible
    message formatting.

    Args:
        text: The text to print. Can be either:
            - A string (used with the color parameter)
            - A list of (text, color) tuples for multi-colored output
        color: The color/style to apply (from Text enum or rich color string).
               Only used when text is a string.
        end: String appended after the text (default: newline).

    Examples:
        # Single color
        cprint("Error occurred!", Text.ERROR)
        cprint("Status: ", Text.INFO, end="")

        # Multi-colored text in one line
        cprint([
            ("Error: ", Text.ERROR),
            ("File not found", Text.WARNING)
        ])

    """
    if isinstance(text, list):
        # Multi-colored mode: build a single rich markup string
        # from a list of (text, color) tuples, then print at once.
        output = ""
        for segment_text, segment_color in text:
            if segment_color:
                output += f"[{segment_color}]{escape(segment_text)}[/{segment_color}]"
            else:
                output += escape(segment_text)
        _console.print(output, end=end)
    else:
        # Single color mode: wrap the entire text in one markup tag.
        if color:
            _console.print(f"[{color}]{escape(text)}[/{color}]", end=end)
        else:
            _console.print(text, end=end)


@contextmanager
def status(message: str, spinner: str = "dots") -> Generator[None, None, None]:
    """Display a status message with a spinner while executing a block of code.

    This is a context manager that shows an animated spinner with a message
    during long-running operations.

    Args:
        message: The status message to display.
        spinner: The spinner style to use (default: "dots").

    Yields:
        None

    Example:
        with status("Copying files..."):
            # Perform long operation
            copy_files()

    """
    with _console.status(message, spinner=spinner):
        yield
