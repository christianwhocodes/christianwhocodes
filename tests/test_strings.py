"""Tests for christianwhocodes.core.strings module.

Covers the two string utility functions:
- generate_random_string: cryptographically secure random string generation
- max_length_from_choices: helper for CLI menu alignment

Run just these tests::

    uv run pytest tests/test_strings.py -v
"""

import pytest

from christianwhocodes.core.strings import (
    generate_random_string,
    max_length_from_choices,
)


class TestGenerateRandomString:
    """Tests for the generate_random_string() function.

    This function is a pure function (no side effects). It generates a
    random string of a given length from a given character set using the
    ``secrets`` module for cryptographic randomness.
    """

    def test_default_length(self) -> None:
        """Default length is 32 characters."""
        result = generate_random_string()
        assert len(result) == 32

    def test_custom_length(self) -> None:
        """Passing length=64 should produce a 64-character string."""
        result = generate_random_string(length=64)
        assert len(result) == 64

    def test_single_char(self) -> None:
        """Edge case: length=1 should still work and return one character."""
        result = generate_random_string(length=1)
        assert len(result) == 1

    def test_custom_charset(self) -> None:
        """When a restricted charset is given, output must only contain those chars."""
        result = generate_random_string(length=100, charset="abc")
        assert all(c in "abc" for c in result)

    def test_zero_length_raises(self) -> None:
        """length=0 is invalid and should raise ValueError."""
        with pytest.raises(ValueError, match="positive"):
            generate_random_string(length=0)

    def test_negative_length_raises(self) -> None:
        """Negative lengths are invalid and should raise ValueError."""
        with pytest.raises(ValueError, match="positive"):
            generate_random_string(length=-5)

    def test_uniqueness(self) -> None:
        """Two random strings should (almost certainly) differ.

        With 62^32 possible strings, a collision is astronomically unlikely.
        """
        a = generate_random_string(length=32)
        b = generate_random_string(length=32)
        assert a != b


class TestMaxLengthFromChoices:
    """Tests for the max_length_from_choices() function.

    Accepts an iterable of (value, display) tuples and returns the
    length of the longest value string. Used for aligning CLI output.
    """

    def test_basic(self) -> None:
        """Should return the length of the longest first element."""
        choices = [("short", "A"), ("very_long_option", "B")]
        assert max_length_from_choices(choices) == 16

    def test_single_choice(self) -> None:
        """Works with a single-element list."""
        assert max_length_from_choices([("hello", "x")]) == 5

    def test_empty_choices(self) -> None:
        """Empty input should return 0 (not raise)."""
        assert max_length_from_choices([]) == 0

    def test_empty_string_choices(self) -> None:
        """Choices with empty strings should return 0."""
        assert max_length_from_choices([("", "x"), ("", "y")]) == 0
