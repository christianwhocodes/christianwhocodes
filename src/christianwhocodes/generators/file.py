"""Configuration file generators for common developer tools."""

from abc import ABC, abstractmethod
from enum import StrEnum
from os import environ
from pathlib import Path
from platform import system

from ..io.console import Text, print, status
from .file import FileGenerator


class FileGenerator(ABC):
    r"""Abstract base class for generating configuration files.

    Provides a template method pattern for file generation with optional
    overwrite confirmation. Subclasses must implement file_path and data
    properties to define where files should be created and their content.

    Example:
        class MyConfigGenerator(FileGenerator):
            @property
            def file_path(self) -> Path:
                return Path("~/.myconfig").expanduser()

            @property
            def data(self) -> str:
                return "# My configuration\\nkey=value\\n"

    """

    @property
    @abstractmethod
    def file_path(self) -> Path:
        """Return the target file path.

        Subclasses must override this to specify where the file should be created.
        """
        ...

    @property
    @abstractmethod
    def data(self) -> str:
        """Return the file content.

        Subclasses must override this to specify what content should be written.
        """
        ...

    def _confirm_overwrite_if_file_exists(self, force: bool = False) -> bool:
        """Check if file exists and prompt for overwrite confirmation.

        Args:
            force: If True, skip confirmation and allow overwrite.

        Returns:
            True if file should be written, False if operation should be aborted.

        """
        if (
            self.file_path.exists()
            and self.file_path.is_file()
            and self.file_path.stat().st_size > 0
            and not force
        ):
            attempts = 0
            while attempts < 3:
                print(
                    f"'{self.file_path}' exists and is not empty",
                    Text.WARNING,
                    force=True,
                )
                resp = input("overwrite? [y/N]: ").strip().lower()
                match resp:
                    case "y" | "yes":
                        return True
                    case "n" | "no" | "":
                        print("Aborted.", Text.WARNING, force=True)
                        return False
                    case _:
                        print("Please answer with 'y' or 'n'.", Text.INFO, force=True)
                        attempts += 1
            print("Too many invalid responses. Aborted.", Text.WARNING, force=True)
            return False
        else:
            return True

    def create(self, force: bool = False) -> bool:
        """Create or overwrite the file with the specified content.

        Creates parent directories if they don't exist and writes the file
        content provided by the data property.

        Args:
            force: If True, overwrite without confirmation.

        Returns:
            True if the file was written, False if the operation was aborted.

        """
        if not self._confirm_overwrite_if_file_exists(force):
            return False  # Abort

        # Ensure parent directory exists
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write data provided by subclass with status indicator
        with status(f"Creating {self.file_path.name}..."):
            self.file_path.write_text(self.data)
        print(f"✓ File written to {self.file_path}", Text.SUCCESS)
        return True


class FileGeneratorOption(StrEnum):
    """Available configuration file generator options.

    Each option corresponds to a specific file generator implementation.

    Attributes:
        PG_SERVICE: PostgreSQL service configuration file (.pg_service.conf).
        PGPASS: PostgreSQL password file (pgpass.conf or .pgpass).
        SSH_CONFIG: SSH configuration file (~/.ssh/config).

    """

    PG_SERVICE = "pg_service"
    PGPASS = "pgpass"
    SSH_CONFIG = "ssh_config"


class PgConfigFilesEnum(StrEnum):
    """Enum for PostgreSQL configuration file names based on platform."""

    PG_SERVICE = ".pg_service.conf"
    PGPASS = "pgpass.conf" if system() == "Windows" else ".pgpass"


class PgServiceFileGenerator(FileGenerator):
    """Generator for PostgreSQL service configuration file.

    Creates a pg_service.conf file in the appropriate location based on the OS:

    - **Windows**: ``%APPDATA%/postgresql/.pg_service.conf``
    - **Unix/Linux/macOS**: ``~/.pg_service.conf``

    The .pg_service.conf file allows referencing named connection profiles
    (e.g. ``service=mydb``) instead of repeating host/port/dbname/user in
    every connection string.

    Example:
        >>> generator = PgServiceFileGenerator()
        >>> generator.create()

    """

    @property
    def file_path(self) -> Path:
        """Return the platform-specific path for the .pg_service.conf file."""
        match system():
            case "Windows":
                return Path(environ["APPDATA"]) / "postgresql" / PgConfigFilesEnum.PG_SERVICE.value
            case _:
                return Path(f"~/{PgConfigFilesEnum.PG_SERVICE.value}").expanduser()

    @property
    def data(self) -> str:
        """Return template content for the .pg_service.conf file."""
        return (
            f"# Read more about {PgConfigFilesEnum.PG_SERVICE.value} file: https://www.postgresql.org/docs/current/libpq-pgservice.html \n\n"
            "# comment\n"
            "[mydb]\n"
            "host=localhost\n"
            "port=5432\n"
            "dbname=postgres\n"
            "user=postgres\n"
        )


class PgPassFileGenerator(FileGenerator):
    """Generator for PostgreSQL password file.

    Creates a .pgpass/pgpass.conf file in the appropriate location based on the OS:

    - **Windows**: ``%APPDATA%/postgresql/pgpass.conf``
    - **Unix/Linux/macOS**: ``~/.pgpass``

    On Unix-like systems the file permissions are automatically set to 600
    (owner read/write only) because PostgreSQL will refuse to use a .pgpass
    file that is readable by other users.

    Example:
        >>> generator = PgPassFileGenerator()
        >>> generator.create()

    """

    @property
    def file_path(self) -> Path:
        """Return the platform-specific path for the .pgpass/pgpass.conf file."""
        match system():
            case "Windows":
                return Path(environ["APPDATA"]) / "postgresql" / PgConfigFilesEnum.PGPASS.value
            case _:
                return Path(f"~/{PgConfigFilesEnum.PGPASS.value}").expanduser()

    @property
    def data(self) -> str:
        """Return template content for the .pgpass/pgpass.conf file."""
        return (
            f"# Read more about {PgConfigFilesEnum.PGPASS.value} file: https://www.postgresql.org/docs/current/libpq-pgpass.html \n\n"
            "# This file should contain lines of the following format:\n"
            "# hostname:port:database:username:password\n"
        )

    def create(self, force: bool = False) -> bool:
        """Create or overwrite .pgpass/pgpass.conf file with strict permissions.

        Args:
            force: If True, overwrite without confirmation.

        Returns:
            True if the file was written, False if the operation was aborted.

        Note:
            On Unix-like systems, this method sets file permissions to 600
            (owner read/write only) as required by PostgreSQL for security.

        """
        from stat import S_IRUSR, S_IWUSR

        # Delegate to the base class for overwrite confirmation and file writing.
        # Only proceed with chmod if the file was actually created.
        if not super().create(force=force):
            return False

        # PostgreSQL refuses to read pgpass files with group/world permissions,
        # so restrict to owner-only (600).  Not needed on Windows which uses ACLs.
        if system() != "Windows":
            try:
                self.file_path.chmod(S_IRUSR | S_IWUSR)  # chmod 600
                print(f"✓ Permissions set to 600 for {self.file_path}", Text.SUCCESS)
            except Exception as e:
                print(
                    f"Warning: could not set permissions on {self.file_path}: {e}",
                    Text.WARNING,
                    force=True,
                )
        return True


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
        """Return template content for the SSH config file."""
        return (
            "# Read more about SSH config files: https://linux.die.net/man/5/ssh_config\n"
            "# ssh -i 'path/to/key' user@domain_or_ip\n\n"
            "Host my_host_alias\n"
            "    IdentityFile path/to/key\n"
            "    User my_user\n"
            "    HostName my_domain_or_ip_address\n"
            "#    LocalForward 8080 localhost:8080\n"
        )


__all__: list[str] = [
    "FileGenerator",
    "FileGeneratorOption",
    "PgServiceFileGenerator",
    "PgPassFileGenerator",
    "SSHConfigFileGenerator",
    "PgConfigFilesEnum",
]
