"""Configuration file generators for common developer tools."""

from os import environ
from pathlib import Path
from platform import system

from ..io.console import Text, print
from .base import FileGenerator


class PgServiceFileGenerator(FileGenerator):
    """Generator for PostgreSQL service configuration file.

    Creates a .pg_service.conf file in the appropriate location based on the OS:
    - Windows: %APPDATA%/postgresql/.pg_service.conf
    - Unix/Linux/macOS: ~/.pg_service.conf

    This file allows storing PostgreSQL connection parameters by service name,
    simplifying connection strings.

    Example:
        >>> generator = PgServiceFileGenerator()
        >>> generator.create()
        File written to /home/user/.pg_service.conf
    """

    @property
    def file_path(self) -> Path:
        """Return the platform-specific path for the pg_service.conf file."""
        match system():
            case "Windows":
                return Path(environ["APPDATA"]) / "postgresql" / ".pg_service.conf"
            case _:
                return Path("~/.pg_service.conf").expanduser()

    @property
    def data(self) -> str:
        """Return template content for pg_service.conf file."""
        return (
            "# Read more about pg_service file: https://www.postgresql.org/docs/current/libpq-pgservice.html\n\n"
            "# comment\n"
            "[mydb]\n"
            "host=localhost\n"
            "port=5432\n"
            "dbname=postgres\n"
            "user=postgres\n"
        )


class PgPassFileGenerator(FileGenerator):
    """Generator for PostgreSQL password file.

    Creates a pgpass file in the appropriate location based on the OS:
    - Windows: %APPDATA%/postgresql/pgpass.conf
    - Unix/Linux/macOS: ~/.pgpass

    On Unix-like systems, automatically sets file permissions to 600 for security
    as required by PostgreSQL.

    Example:
        >>> generator = PgPassFileGenerator()
        >>> generator.create()
        File written to /home/user/.pgpass
        Permissions set to 600 for /home/user/.pgpass
    """

    @property
    def file_path(self) -> Path:
        """Return the platform-specific path for the pgpass file."""
        match system():
            case "Windows":
                return Path(environ["APPDATA"]) / "postgresql" / "pgpass.conf"
            case _:
                return Path("~/.pgpass").expanduser()

    @property
    def data(self) -> str:
        """Return template content for pgpass file."""
        return (
            "# Read more about pgpass file: https://www.postgresql.org/docs/current/libpq-pgpass.html\n\n"
            "# This file should contain lines of the following format:\n"
            "# hostname:port:database:username:password\n"
        )

    def create(self, force: bool = False) -> None:
        """Create or overwrite pgpass file with strict permissions.

        Args:
            force: If True, overwrite without confirmation.

        Note:
            On Unix-like systems, this method sets file permissions to 600
            (owner read/write only) as required by PostgreSQL for security.
        """
        from stat import S_IRUSR, S_IWUSR

        super().create(force=force)

        # Set strict permissions on Unix-like systems
        if system() != "Windows":
            try:
                self.file_path.chmod(S_IRUSR | S_IWUSR)  # chmod 600
                print(f"✓ Permissions set to 600 for {self.file_path}", Text.SUCCESS)
            except Exception as e:
                print(
                    f"Warning: could not set permissions on {self.file_path}: {e}",
                    Text.WARNING,
                )


class SSHConfigFileGenerator(FileGenerator):
    """Generator for SSH configuration file.

    Creates an SSH config file at ~/.ssh/config with a template host configuration.
    This file allows defining SSH connection shortcuts and settings.

    Example:
        >>> generator = SSHConfigFileGenerator()
        >>> generator.create()
        File written to /home/user/.ssh/config
    """

    @property
    def file_path(self) -> Path:
        """Return the path for the SSH config file (~/.ssh/config)."""
        return Path("~/.ssh/config").expanduser()

    @property
    def data(self) -> str:
        """Return template content for SSH config file."""
        return (
            "# Read more about SSH config files: https://linux.die.net/man/5/ssh_config\n"
            "# ssh -i 'path/to/key' user@domain_or_ip\n\n"
            "Host my_host_alias\n"
            "    IdentityFile D:/.ssh/key\n"
            "    User my_user\n"
            "    HostName my_domain_or_ip_address\n"
            "#    LocalForward 8080 localhost:8080\n"
        )


__all__: list[str] = [
    "PgServiceFileGenerator",
    "PgPassFileGenerator",
    "SSHConfigFileGenerator",
]
