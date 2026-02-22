"""Configuration file generators for common developer tools."""

from dataclasses import dataclass
from pathlib import Path

from ..io import Text, cprint, status
from ..utils import Platform

__all__: list[str] = [
    "FileSpec",
    "get_pg_service_spec",
    "get_pgpass_spec",
    "get_ssh_config_spec",
    "FileGenerator",
]


@dataclass
class FileSpec:
    """Defines the path, content, and security requirements of a config file."""

    path: Path
    content: str
    chmod_mode: int | None = None


def _pg_base_path() -> Path:
    from os import getenv

    if Platform().os_name == "windows":
        appdata = getenv("APPDATA", str(Path.home()))
        return Path(appdata) / "postgresql"
    return Path.home()


def get_pg_service_spec() -> FileSpec:
    """Return the FileSpec for a PostgreSQL service connection file (~/.pg_service.conf)."""
    content = (
        "# Read more: https://www.postgresql.org/docs/current/libpq-pgservice.html\n\n"
        "[mydb]\n"
        "host=localhost\n"
        "port=5432\n"
        "dbname=postgres\n"
        "user=postgres\n"
    )
    return FileSpec(path=_pg_base_path() / ".pg_service.conf", content=content)


def get_pgpass_spec() -> FileSpec:
    """Return the FileSpec for a PostgreSQL password file (~/.pgpass or pgpass.conf on Windows)."""
    from stat import S_IRUSR, S_IWUSR

    is_win = Platform().os_name == "windows"
    filename = "pgpass.conf" if is_win else ".pgpass"
    content = (
        "# Read more: https://www.postgresql.org/docs/current/libpq-pgpass.html\n\n"
        "# hostname:port:database:username:password\n"
    )
    mode = None if is_win else (S_IRUSR | S_IWUSR)
    return FileSpec(path=_pg_base_path() / filename, content=content, chmod_mode=mode)


def get_ssh_config_spec() -> FileSpec:
    """Return the FileSpec for an SSH client configuration file (~/.ssh/config)."""
    content = (
        "# Read more: https://linux.die.net/man/5/ssh_config\n\n"
        "Host my_host_alias\n"
        "    IdentityFile ~/.ssh/id_rsa\n"
        "    User my_user\n"
        "    HostName my_domain_or_ip_address\n"
    )
    return FileSpec(path=Path.home() / ".ssh" / "config", content=content)


class FileGenerator:
    """Handles the actual file I/O operations and permissions."""

    def __init__(self, spec: FileSpec):
        """Initialize the generator with a file specification."""
        self.spec = spec

    def create(self, overwrite: bool = False) -> bool:
        """Write the file to disk, applying permissions if specified.

        Args:
            overwrite: If True, skip confirmation and overwrite existing files.

        Returns:
            True if the file was written successfully, False if aborted.

        """
        if not self._should_overwrite(overwrite):
            return False

        self.spec.path.parent.mkdir(parents=True, exist_ok=True)

        with status(f"Creating {self.spec.path.name}..."):
            self.spec.path.write_text(self.spec.content)

        cprint(f"✓ File written to {self.spec.path}", Text.SUCCESS)

        # Apply specific permissions if required by the file spec
        if self.spec.chmod_mode is not None:
            try:
                self.spec.path.chmod(self.spec.chmod_mode)
                octal_mode = oct(self.spec.chmod_mode)[2:]
                cprint(f"✓ Permissions secured for {self.spec.path} ({octal_mode})", Text.SUCCESS)
            except Exception as e:
                cprint(f"Warning: could not set permissions on {self.spec.path}: {e}", Text.WARNING)

        return True

    def _should_overwrite(self, overwrite: bool) -> bool:
        """Determine whether to proceed, prompting the user if the file already exists.

        Returns:
            True to proceed with writing, False to abort.

        """
        if not self.spec.path.exists() or self.spec.path.stat().st_size == 0 or overwrite:
            # File doesn't exist, is empty, or overwrite is forced - no confirmation needed.
            return True

        for _ in range(3):
            # File exists and is not empty - ask for confirmation. Limit to 3 attempts to avoid infinite loops.
            cprint(f"'{self.spec.path}' exists and is not empty", Text.WARNING)
            resp = input("overwrite? [y/N]: ").strip().lower()
            if resp in ("y", "yes"):
                return True
            if resp in ("n", "no", ""):
                cprint("Aborted.", Text.WARNING)
                return False
            cprint("Please answer with 'y' or 'n'.", Text.INFO)

        cprint("Too many invalid responses. Aborted.", Text.WARNING)
        return False
