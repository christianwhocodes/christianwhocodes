"""Version management and retrieval utilities."""

from typing import Literal

from .enums import ExitCode


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
    def get(package: str) -> tuple[str, str]:
        """Get the installed version of a package.

        Args:
            package: Name of the package to get version for.

        Returns:
            Tuple of (version_string, error_message).
            If successful, error_message is empty.
            If failed, version_string is the placeholder and error_message contains details.
        """
        try:
            from importlib.metadata import version

            return version(package), ""
        except Exception as e:
            return (
                Version.placeholder(),
                f"Could not determine version\n{str(e)}",
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


__all__: list[str] = ["Version", "print_version"]
