"""Tests for christianwhocodes.core.urls module.

Covers the normalize_url_path() function which ensures consistent leading/trailing
slash usage and collapses duplicate slashes in URL path segments.

Run just these tests::

    uv run pytest tests/test_urls.py -v
"""

from christianwhocodes.core.urls import normalize_url_path


class TestNormalizeUrlPath:
    """Tests for the normalize_url_path() function.

    Parameters
    ----------
        url: The raw URL path string.
        leading_slash: Whether to enforce a leading ``/`` (default: False).
        trailing_slash: Whether to enforce a trailing ``/`` (default: True).

    """

    def test_default_trailing_slash(self) -> None:
        """By default, a trailing slash is added."""
        assert normalize_url_path("api/users") == "api/users/"

    def test_no_trailing_slash(self) -> None:
        """trailing_slash=False strips the trailing slash."""
        assert normalize_url_path("api/users/", trailing_slash=False) == "api/users"

    def test_leading_slash(self) -> None:
        """leading_slash=True prepends a slash."""
        assert normalize_url_path("api/users", leading_slash=True) == "/api/users/"

    def test_both_slashes(self) -> None:
        """Both flags together produce '/api/'."""
        result = normalize_url_path("api", leading_slash=True, trailing_slash=True)
        assert result == "/api/"

    def test_neither_slash(self) -> None:
        """Both False strips both leading and trailing slashes."""
        result = normalize_url_path("/api/", leading_slash=False, trailing_slash=False)
        assert result == "api"

    def test_collapses_multiple_slashes(self) -> None:
        """Consecutive slashes like '//api//users//' are collapsed to single slashes."""
        result = normalize_url_path("//api//users//", leading_slash=True, trailing_slash=False)
        assert result == "/api/users"

    def test_empty_string(self) -> None:
        """Empty string always returns '/' as a safe default."""
        assert normalize_url_path("") == "/"

    def test_single_slash_no_trailing(self) -> None:
        """Edge case: '/' with trailing_slash=False should still return '/' (never return an empty string)."""
        result = normalize_url_path("/", leading_slash=True, trailing_slash=False)
        assert result == "/"

    def test_single_slash_no_leading(self) -> None:
        """Edge case: '/' with both False should still return '/' (never return an empty string)."""
        result = normalize_url_path("/", leading_slash=False, trailing_slash=False)
        assert result == "/"
