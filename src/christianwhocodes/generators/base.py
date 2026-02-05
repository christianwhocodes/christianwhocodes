"""Base classes for file generation functionality."""

from abc import ABC, abstractmethod
from enum import StrEnum
from pathlib import Path

from ..io.console import Text, print


class FileGenerator(ABC):
    """Abstract base class for generating configuration files.

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
                print(f"'{self.file_path}' exists and is not empty", Text.WARNING)
                resp = input("overwrite? [y/N]: ").strip().lower()
                match resp:
                    case "y" | "yes":
                        return True
                    case "n" | "no" | "":
                        print("Aborted.", Text.WARNING)
                        return False
                    case _:
                        print("Please answer with 'y' or 'n'.", Text.INFO)
                        attempts += 1
            print("Too many invalid responses. Aborted.", Text.WARNING)
            return False
        else:
            return True

    def create(self, force: bool = False) -> None:
        """Create or overwrite the file with the specified content.

        Creates parent directories if they don't exist and writes the file
        content provided by the data property.

        Args:
            force: If True, overwrite without confirmation.
        """
        if not self._confirm_overwrite_if_file_exists(force):
            return  # Abort

        # Ensure parent directory exists
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

        # Write data provided by subclass
        self.file_path.write_text(self.data)
        print(f"File written to {self.file_path}", Text.SUCCESS)


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


__all__: list[str] = ["FileGenerator", "FileGeneratorOption"]
