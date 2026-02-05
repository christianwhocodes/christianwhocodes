"""Platform and architecture detection utilities."""

from platform import machine, system


class PlatformInfo:
    """Encapsulates platform and architecture information.

    Detects the operating system and CPU architecture, normalizing them
    to standard identifiers for cross-platform compatibility.

    Attributes:
        os_name: Normalized operating system name (macos, linux, windows).
        architecture: Normalized CPU architecture (x64, arm64).
    """

    PLATFORM_MAP = {
        "darwin": "macos",
        "linux": "linux",
        "windows": "windows",
    }

    ARCH_MAP = {
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


__all__: list[str] = ["PlatformInfo"]
