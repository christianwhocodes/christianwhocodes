"""Version management and retrieval utilities."""

from typing import Literal, NamedTuple

from .enums import ExitCode


class VersionResult(NamedTuple):
    """Result of a version lookup.

    Attributes:
        version: The version string, or a placeholder if lookup failed.
        error: Empty string on success, error details on failure.
    """

    version: str
    error: str


class Version:
    """Utility class for version-related operations."""

    @staticmethod
    def placeholder() -> Literal["X.Y.Z"]:
        """Return a version placeholder string.

        Returns:
            The literal placeholder version string "X.Y.Z".
        """
        return "X.Y.Z"

    @staticmethod
    def get(package: str) -> VersionResult:
        """Get the installed version of a package.

        Args:
            package: Name of the package to get version for.

        Returns:
            VersionResult with version string and error message.
            If successful, error is empty.
            If failed, version is the placeholder and error contains details.
        """
        try:
            from importlib.metadata import version

            return VersionResult(version(package), "")
        except Exception as e:
            return VersionResult(
                Version.placeholder(),
                f"Could not determine version\n{e}",
            )


def print_version(package: str) -> ExitCode:
    """Print the package version and return appropriate exit code.

    Args:
        package: Name of the package to get version for.

    Returns:
        ExitCode.SUCCESS (0) if version found, ExitCode.ERROR (1) otherwise.

    Example:
        >>> print_version("christianwhocodes")
        1.2.7
        ExitCode.SUCCESS
    """
    # Import here to avoid circular dependency
    from ..io import print

    version_string, error_msg = Version.get(package)

    if version_string != Version.placeholder():
        print(version_string)
        return ExitCode.SUCCESS
    else:
        print(f"{version_string}: Could not determine version for package '{package}'.")
        if error_msg:
            print(error_msg)
        return ExitCode.ERROR


__all__: list[str] = ["Version", "VersionResult", "print_version"]
