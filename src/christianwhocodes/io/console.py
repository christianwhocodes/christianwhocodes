"""Console output utilities for rich-formatted text."""

from enum import StrEnum
from typing import Optional

from rich.console import Console
from rich.theme import Theme


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


def print(
    text: str | list[tuple[str, Optional[str]]],
    color: Optional[str] = None,
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
        print("Error occurred!", Text.ERROR)
        print("Status: ", Text.INFO, end="")

        # Multi-colored text in one line
        print([
            ("Error: ", Text.ERROR),
            ("File not found", Text.WARNING)
        ])
    """
    if isinstance(text, list):
        # Multi-colored mode: text is a list of (text, color) tuples
        output = ""
        for segment_text, segment_color in text:
            if segment_color:
                output += f"[{segment_color}]{segment_text}[/{segment_color}]"
            else:
                output += segment_text
        _console.print(output, end=end)
    else:
        # Single color mode
        if color:
            _console.print(f"[{color}]{text}[/{color}]", end=end)
        else:
            _console.print(text, end=end)


__all__: list[str] = ["Text", "print"]
