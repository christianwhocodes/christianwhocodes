"""Tests for christianwhocodes.core.config module.

Covers the PyProject class which parses pyproject.toml files and exposes
project metadata (name, version, authors, dependencies, etc.) via properties.

These tests use the project's own pyproject.toml as a real-world fixture,
plus tmp_path for error-case testing.

Run just these tests::

    uv run pytest tests/test_config.py -v
"""

from pathlib import Path

import pytest

from christianwhocodes.core.config import PyProject

# Use the project's own pyproject.toml as a real-world test fixture.
# Path(__file__).parent is tests/, so .parent again gives the repo root.
_PYPROJECT_PATH = Path(__file__).parent.parent / "pyproject.toml"


class TestPyProject:
    """Tests for the PyProject class.

    Most tests load _PYPROJECT_PATH (this project's real pyproject.toml)
    and verify that the parsed properties match expected values.
    """

    def test_load(self) -> None:
        """Loading a valid pyproject.toml should populate the name field."""
        py = PyProject(_PYPROJECT_PATH)
        assert py.name == "christianwhocodes"

    def test_version(self) -> None:
        """Version should be a non-empty string (exact value may change)."""
        py = PyProject(_PYPROJECT_PATH)
        assert py.version  # truthy = non-empty string

    def test_description(self) -> None:
        """Description should match the value in pyproject.toml."""
        py = PyProject(_PYPROJECT_PATH)
        assert py.description == "Python utilities for developers."

    def test_authors(self) -> None:
        """Authors should be a non-empty list of dicts with a 'name' key."""
        py = PyProject(_PYPROJECT_PATH)
        assert len(py.authors) > 0
        assert "name" in py.authors[0]

    def test_dependencies(self) -> None:
        """Dependencies should be a non-empty list of requirement strings."""
        py = PyProject(_PYPROJECT_PATH)
        assert isinstance(py.dependencies, list)
        assert len(py.dependencies) > 0

    def test_python_requires(self) -> None:
        """The requires-python field should reference Python 3.12+."""
        py = PyProject(_PYPROJECT_PATH)
        assert py.python_requires is not None
        assert "3.12" in py.python_requires

    def test_data_returns_full_dict(self) -> None:
        """The raw .data property should contain both [project] and [build-system]."""
        py = PyProject(_PYPROJECT_PATH)
        assert "project" in py.data
        assert "build-system" in py.data

    def test_path_property(self) -> None:
        """The .path property should match the path passed to the constructor."""
        py = PyProject(_PYPROJECT_PATH)
        assert py.path == _PYPROJECT_PATH

    def test_missing_file_raises(self) -> None:
        """A non-existent file should raise FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            PyProject(Path("/nonexistent/pyproject.toml"))

    def test_missing_project_section_raises(self, tmp_path: Path) -> None:
        """A TOML file without a [project] section should raise KeyError.

        Uses pytest's tmp_path fixture to create a temporary TOML file
        that has [build-system] but no [project].
        """
        toml_file = tmp_path / "pyproject.toml"
        toml_file.write_text("[build-system]\nrequires = []\n")
        with pytest.raises(KeyError, match="project"):
            PyProject(toml_file)
