"""Tests for christianwhocodes.core.platform module.

Covers the Platform class which auto-detects the current OS and CPU architecture
and normalizes them to standard identifiers (e.g. 'windows-x64', 'linux-arm64').

Run just these tests::

    uv run pytest tests/test_platform.py -v
"""

from christianwhocodes.core.platform import Platform


class TestPlatform:
    """Tests for the Platform class.

    Since Platform detects the *current* machine, tests verify that the
    detected values are within the set of known valid values rather than
    asserting a specific OS/architecture.
    """

    def test_detection(self) -> None:
        """OS should be one of macos/linux/windows, arch one of x64/arm64."""
        p = Platform()
        assert p.os_name in ("macos", "linux", "windows")
        assert p.architecture in ("x64", "arm64")

    def test_str_format(self) -> None:
        """str(Platform()) should produce 'os-architecture' format."""
        p = Platform()
        assert str(p) == f"{p.os_name}-{p.architecture}"

    def test_repr(self) -> None:
        """repr() should include the class name and both attributes."""
        p = Platform()
        r = repr(p)
        assert "Platform(" in r
        assert p.os_name in r
        assert p.architecture in r

    def test_equality(self) -> None:
        """Two Platform instances on the same machine should be equal."""
        a = Platform()
        b = Platform()
        assert a == b

    def test_inequality_with_other_type(self) -> None:
        """Comparing Platform to a non-Platform should return NotImplemented
        (which Python interprets as not equal)."""
        p = Platform()
        assert p != "not a platform"

    def test_hashable(self) -> None:
        """Platform instances should be usable as dict keys and in sets."""
        p = Platform()
        s = {p}
        assert p in s
