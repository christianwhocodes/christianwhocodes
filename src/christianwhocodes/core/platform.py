"""Platform and architecture detection utilities."""

from platform import machine, system
from typing import ClassVar


class Platform:
    """Encapsulates platform and architecture information.

    Detects the operating system and CPU architecture, normalizing them
    to standard identifiers for cross-platform compatibility.

    Attributes:
        os_name: Normalized operating system name (macos, linux, windows).
        architecture: Normalized CPU architecture (x64, arm64).
    """

    PLATFORM_MAP: ClassVar[dict[str, str]] = {
        "darwin": "macos",
        "linux": "linux",
        "windows": "windows",
    }

    ARCH_MAP: ClassVar[dict[str, str]] = {
        "x86_64": "x64",
        "amd64": "x64",
        "x64": "x64",
        "arm64": "arm64",
        "aarch64": "arm64",
        "armv8": "arm64",
    }

    def __init__(self) -> None:
        """Initialize platform detection."""
        self.os_name = self._detect_os()
        self.architecture = self._detect_architecture()

    def _detect_os(self) -> str:
        """Detect and validate the operating system.

        Returns:
            Normalized OS name.

        Raises:
            OSError: If the operating system is not supported.
        """
        system_platform = system().lower()
        platform_name = self.PLATFORM_MAP.get(system_platform)

        if not platform_name:
            raise OSError(
                f"Unsupported operating system: {system_platform}. "
                f"Supported: {', '.join(self.PLATFORM_MAP.values())}"
            )

        return platform_name

    def _detect_architecture(self) -> str:
        """Detect and validate the system architecture.

        Returns:
            Normalized architecture name.

        Raises:
            ValueError: If the architecture is not supported.
        """
        machine_platform = machine().lower()
        architecture = self.ARCH_MAP.get(machine_platform)

        if not architecture:
            raise ValueError(
                f"Unsupported architecture: {machine_platform}. "
                f"Supported: {', '.join(set(self.ARCH_MAP.values()))}"
            )

        return architecture

    def __str__(self) -> str:
        """Return string representation in format 'os-architecture'."""
        return f"{self.os_name}-{self.architecture}"

    def __repr__(self) -> str:
        """Return detailed string representation for debugging.

        Without this, repr() would show something unhelpful like
        ``<Platform object at 0x7f...>``.  With it you get a readable,
        copy-pasteable representation.

        Example::

            >>> p = Platform()
            >>> repr(p)
            "Platform(os_name='windows', architecture='x64')"

            >>> p          # in the REPL / debugger, __repr__ is called automatically
            Platform(os_name='windows', architecture='x64')
        """
        return f"Platform(os_name={self.os_name!r}, architecture={self.architecture!r})"

    def __eq__(self, other: object) -> bool:
        """Check equality based on OS name and architecture.

        Without this, ``==`` compares memory addresses, so two Platform
        instances on the same machine would be considered *not* equal.
        With it, equality is determined by matching os_name and architecture.

        Example::

            >>> a = Platform()
            >>> b = Platform()
            >>> a == b          # True — same OS and architecture
            True

            >>> a == "windows"  # comparing to a non-Platform returns NotImplemented
            False               # (Python falls back to False)
        """
        if not isinstance(other, Platform):
            return NotImplemented
        return self.os_name == other.os_name and self.architecture == other.architecture

    def __hash__(self) -> int:
        """Return hash based on OS name and architecture.

        Once ``__eq__`` is defined, Python makes the class unhashable by
        default.  This re-enables hashing so Platform instances can be
        used in sets and as dictionary keys.

        Example::

            >>> p = Platform()

            >>> # Use as a dictionary key
            >>> downloads = {p: "https://example.com/app-windows-x64.zip"}
            >>> downloads[Platform()]
            'https://example.com/app-windows-x64.zip'

            >>> # Use in a set (duplicates are automatically removed)
            >>> platforms = {Platform(), Platform()}
            >>> len(platforms)
            1
        """
        return hash((self.os_name, self.architecture))


__all__: list[str] = ["Platform"]
