from platform import machine, system


class PlatformInfo:
    """Encapsulates platform and architecture information."""

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
        self.os_name = self._detect_os()
        self.architecture = self._detect_architecture()

    def _detect_os(self) -> str:
        """Detect and validate the operating system."""
        system_platform = system().lower()
        platform_name = self.PLATFORM_MAP.get(system_platform)

        if not platform_name:
            raise OSError(
                f"Unsupported operating system: {system_platform}. "
                f"Supported: {', '.join(self.PLATFORM_MAP.values())}"
            )

        return platform_name

    def _detect_architecture(self) -> str:
        """Detect and validate the system architecture."""
        machine_platform = machine().lower()
        architecture = self.ARCH_MAP.get(machine_platform)

        if not architecture:
            raise ValueError(
                f"Unsupported architecture: {machine_platform}. "
                f"Supported: {', '.join(set(self.ARCH_MAP.values()))}"
            )

        return architecture

    def __str__(self) -> str:
        return f"{self.os_name}-{self.architecture}"


__all__: list[str] = ["PlatformInfo"]
