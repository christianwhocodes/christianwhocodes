"""Configuration file parsing utilities."""

from pathlib import Path
from typing import Any


__all__: list[str] = ["PyProject"]


class PyProject:
    """Represents the data from a pyproject.toml file.

    Provides convenient property-based access to common project metadata
    while allowing raw access to the full TOML data structure.

    Attributes:
        path: The path to the pyproject.toml file.
        data: The complete parsed TOML data.

    Example:
        >>> py = PyProject(Path("pyproject.toml"))
        >>> py.name
        'my-package'
        >>> py.version
        '1.0.0'
        >>> py.dependencies
        ['requests>=2.28.0', 'rich>=13.0.0']

    """

    def __init__(self, toml_path: Path) -> None:
        """Load and parse the pyproject.toml file.

        Args:
            toml_path: Path to the pyproject.toml file.

        Raises:
            FileNotFoundError: If the file does not exist.
            tomllib.TOMLDecodeError: If the file is invalid TOML.
            KeyError: If the [project] section is missing.

        """
        from tomllib import load

        self._toml_path = toml_path

        with open(toml_path, "rb") as f:
            full_data = load(f)

        if "project" not in full_data:
            raise KeyError(f"[project] section not found in {toml_path}")

        self._data: dict[str, Any] = full_data

    # ============================================================================
    # Project Metadata Properties
    # ============================================================================

    @property
    def name(self) -> str:
        """Return the project name.

        Raises:
            KeyError: If the name field is missing.

        """
        return self._data["project"]["name"]

    @property
    def version(self) -> str:
        """Return the project version.

        Raises:
            KeyError: If the version field is missing.

        """
        return self._data["project"]["version"]

    @property
    def description(self) -> str | None:
        """Return the project description, if any."""
        return self._data["project"].get("description")

    @property
    def authors(self) -> list[dict[str, str]]:
        """Return a list of project authors."""
        return self._data["project"].get("authors", [])

    @property
    def dependencies(self) -> list[str]:
        """Return project dependencies."""
        return self._data["project"].get("dependencies", [])

    @property
    def python_requires(self) -> str | None:
        """Return the required Python version."""
        return self._data["project"].get("requires-python")

    # ============================================================================
    # General Accessors
    # ============================================================================

    @property
    def data(self) -> dict[str, Any]:
        """Return the raw parsed TOML data."""
        return self._data

    @property
    def path(self) -> Path:
        """Return the path to the pyproject.toml file."""
        return self._toml_path
