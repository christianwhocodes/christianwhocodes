"""Console output utilities for rich-formatted text."""

from contextlib import contextmanager
from enum import StrEnum
from typing import Generator, Optional

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
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


@contextmanager
def progress_bar() -> Generator[Progress, None, None]:
    """Create a progress bar context for tracking operations.

    Returns a Progress instance that can be used to track tasks with
    progress updates.

    Yields:
        Progress: A rich Progress instance for tracking tasks.

    Example:
        with progress_bar() as progress:
            task = progress.add_task("Processing...", total=100)
            for i in range(100):
                progress.update(task, advance=1)
    """
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        _console=_console,
    ) as progress:
        yield progress


__all__: list[str] = ["Text", "print", "status", "progress_bar"]
