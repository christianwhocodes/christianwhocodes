"""Tests for christianwhocodes.core.version module.

Covers the Version utility class and VersionResult named tuple:
- Version.placeholder(): returns the fallback version string "X.Y.Z"
- Version.get(package): looks up installed package version via importlib.metadata
- VersionResult: named tuple with .version and .error fields

Run just these tests::

    uv run pytest tests/test_version.py -v
"""

from christianwhocodes.core.version import Version, VersionResult


class TestVersion:
    """Tests for the Version class and VersionResult named tuple."""

    def test_placeholder(self) -> None:
        """The placeholder string is always 'X.Y.Z'."""
        assert Version.placeholder() == "X.Y.Z"

    def test_get_known_package(self) -> None:
        """Looking up an installed package should return a real version and an empty error string."""
        result = Version.get("christianwhocodes")
        assert isinstance(result, VersionResult)
        assert result.version != Version.placeholder()
        assert result.error == ""

    def test_get_unknown_package(self) -> None:
        """Looking up a non-existent package should return the placeholder version and a non-empty error message."""
        result = Version.get("definitely-not-a-real-package-xyz")
        assert result.version == Version.placeholder()
        assert result.error != ""

    def test_version_result_unpacking(self) -> None:
        """VersionResult is a NamedTuple, so it supports tuple unpacking.

        This ensures backward compatibility with code that does:
            version, error = Version.get("pkg")
        """
        version, error = Version.get("christianwhocodes")
        assert isinstance(version, str)
        assert isinstance(error, str)
