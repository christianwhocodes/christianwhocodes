"""Type conversion utilities for common data transformations."""

from pathlib import Path
from typing import Any, Callable, Optional, cast


class TypeConverter:
    """Utility class for converting between common data types."""

    @staticmethod
    def to_bool(value: str | bool) -> bool:
        """Convert a string or boolean to a boolean.

        Args:
            value: String or boolean to convert.

        Returns:
            True if value is truthy, False otherwise.

        Note:
            Truthy strings: 'true', '1', 'yes', 'on' (case-insensitive).
        """
        if isinstance(value, bool):
            return value
        return value.lower() in ("true", "1", "yes", "on")

    @staticmethod
    def to_list_of_str(
        value: Any, transform: Optional[Callable[[str], str]] = None
    ) -> list[str]:
        """Convert a value into a list of strings.

        Args:
            value: List or comma-separated string to convert.
            transform: Optional function to transform each string (e.g., str.lower).

        Returns:
            List of strings.

        Example:
            >>> TypeConverter.to_list_of_str("a, b, c")
            ['a', 'b', 'c']
            >>> TypeConverter.to_list_of_str("A,B,C", str.lower)
            ['a', 'b', 'c']
        """
        result: list[str] = []

        if isinstance(value, list):
            list_value = cast(list[Any], value)
            result = [str(item) for item in list_value]

        elif isinstance(value, str):
            result = [item.strip() for item in value.split(",") if item.strip()]

        if transform:
            result = [transform(item) for item in result]

        return result

    @staticmethod
    def to_path(value: str | Path, resolve: bool = True) -> Path:
        """Convert a string or Path to a properly expanded and resolved Path.

        Handles:
        - User home directory expansion (~)
        - Environment variable expansion ($VAR, ${VAR})
        - Absolute path resolution
        - Relative path resolution (optional)

        Args:
            value: String path or Path object to convert.
            resolve: If True, resolve to absolute path (default: True).

        Returns:
            Processed Path object.

        Examples:
            >>> TypeConverter.to_path("~/documents/file.txt")
            PosixPath('/home/user/documents/file.txt')
            >>> TypeConverter.to_path("$HOME/file.txt")
            PosixPath('/home/user/file.txt')
            >>> TypeConverter.to_path("./relative/path", resolve=False)
            PosixPath('relative/path')
        """
        from os.path import expandvars

        # Convert to Path if string
        if isinstance(value, str):
            path = Path(value)
        else:
            path = value

        # Expand user home directory (~)
        if "~" in str(path):
            path = path.expanduser()

        # Expand environment variables
        path_str = str(path)
        if "$" in path_str:
            path = Path(expandvars(path_str))

        # Resolve to absolute path if requested
        if resolve:
            path = path.resolve()

        return path


__all__: list[str] = ["TypeConverter"]
