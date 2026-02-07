"""Tests for christianwhocodes.core.converters module.

Covers all static methods on the TypeConverter class:
- to_bool: string/bool → bool conversion
- to_list_of_str: string/list → list[str] with optional transform
- to_path: string/Path → resolved Path with ~ and $VAR expansion

Run just these tests::

    uv run pytest tests/test_converters.py -v
"""

from pathlib import Path

from christianwhocodes.core.converters import TypeConverter


class TestToBool:
    """Tests for TypeConverter.to_bool().

    Truthy strings: 'true', '1', 'yes', 'on' (case-insensitive).
    Everything else (including empty string) is False.
    """

    def test_true_strings(self) -> None:
        """All recognized truthy string variants should return True."""
        for val in ("true", "True", "TRUE", "1", "yes", "Yes", "on", "ON"):
            assert TypeConverter.to_bool(val) is True

    def test_false_strings(self) -> None:
        """Unrecognized and falsy strings should return False."""
        for val in ("false", "False", "0", "no", "off", "random", ""):
            assert TypeConverter.to_bool(val) is False

    def test_bool_passthrough(self) -> None:
        """Actual bool values should pass through unchanged."""
        assert TypeConverter.to_bool(True) is True
        assert TypeConverter.to_bool(False) is False


class TestToListOfStr:
    """Tests for TypeConverter.to_list_of_str().

    Accepts either a comma-separated string or a list, and optionally
    applies a transform function to each element.
    """

    def test_comma_separated(self) -> None:
        """A comma-separated string is split and each item stripped."""
        assert TypeConverter.to_list_of_str("a, b, c") == ["a", "b", "c"]

    def test_list_input(self) -> None:
        """A list of strings is returned as-is."""
        assert TypeConverter.to_list_of_str(["a", "b"]) == ["a", "b"]

    def test_list_with_non_strings(self) -> None:
        """Non-string list items are converted via str()."""
        assert TypeConverter.to_list_of_str([1, 2, 3]) == ["1", "2", "3"]

    def test_with_transform(self) -> None:
        """An optional transform (e.g. str.lower) is applied to each item."""
        assert TypeConverter.to_list_of_str("A,B,C", str.lower) == ["a", "b", "c"]

    def test_empty_string(self) -> None:
        """Empty string should return an empty list (not [''])."""
        assert TypeConverter.to_list_of_str("") == []

    def test_empty_list(self) -> None:
        """Empty list input returns empty list."""
        assert TypeConverter.to_list_of_str([]) == []

    def test_strips_whitespace(self) -> None:
        """Leading/trailing whitespace around items is stripped."""
        assert TypeConverter.to_list_of_str("  a , b , c  ") == ["a", "b", "c"]

    def test_unsupported_type(self) -> None:
        """Unsupported types (e.g. int) return an empty list gracefully."""
        assert TypeConverter.to_list_of_str(42) == []


class TestToPath:
    """Tests for TypeConverter.to_path().

    Handles ~ expansion, $VAR expansion, and optional resolve to absolute path.
    """

    def test_string_to_path(self) -> None:
        """A plain string is converted to a Path object."""
        result = TypeConverter.to_path("some/path", resolve=False)
        assert isinstance(result, Path)

    def test_path_passthrough(self) -> None:
        """An existing Path object is accepted and returned (type preserved)."""
        p = Path("some/path")
        result = TypeConverter.to_path(p, resolve=False)
        assert isinstance(result, Path)

    def test_resolve_produces_absolute(self) -> None:
        """With resolve=True (default), the result is always an absolute path."""
        result = TypeConverter.to_path("relative/path", resolve=True)
        assert result.is_absolute()

    def test_no_resolve(self) -> None:
        """With resolve=False, relative paths stay relative."""
        result = TypeConverter.to_path("relative/path", resolve=False)
        # Platform-dependent separator: '/' on Unix, '\\' on Windows
        assert str(result) == "relative\\path" or str(result) == "relative/path"
