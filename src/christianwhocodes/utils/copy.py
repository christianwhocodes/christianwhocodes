"""Utility module for copying files and directories.

This module provides classes and functions to copy files and directories
recursively with appropriate error handling and user prompts.
It replaces the Django management command implementation with a pure Python
implementation using the project's styling utilities.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from shutil import copy2, copytree, rmtree
from typing import Union

from .stdout import Text, print
from .types import TypeConverter

# Type for path-like objects (str or Path)
PathLike = Union[str, Path]


class Copier(ABC):
    """Base class for copy operations.

    This abstract class defines the interface for copying files or directories.
    Subclasses must implement the copy method for specific copy strategies.
    """

    @abstractmethod
    def copy(self, source: Path, destination: Path) -> bool:
        """Execute the copy operation.

        Args:
            source: Source path to copy from.
            destination: Destination path to copy to.

        Returns:
            True if the copy operation was successful, False otherwise.
        """
        pass

    def _validate_source(self, source: Path) -> bool:
        """Validate that source exists and is accessible.

        Args:
            source: The source path to validate.

        Returns:
            True if source exists and is valid, False otherwise.
        """
        if not source.exists():
            print(f"Source path does not exist: {source}", Text.ERROR)
            return False
        return True


class FileCopier(Copier):
    """Copier for individual files.

    Handles copying of single files while preserving metadata and creating
    necessary parent directories at the destination.

    Example:
        copier = FileCopier()
        copier.copy(Path("source.txt"), Path("dest/source.txt"))
    """

    def copy(self, source: Path, destination: Path) -> bool:
        """Copy a single file.

        Preserves file metadata and creates parent directories as needed.
        Uses shutil.copy2 for metadata preservation.

        Args:
            source: Path to the source file.
            destination: Path where the file should be copied to.

        Returns:
            True if the file was copied successfully, False otherwise.
        """
        if not self._validate_source(source):
            return False

        if not source.is_file():
            print(f"Source is not a file: {source}", Text.ERROR)
            return False

        try:
            destination.parent.mkdir(parents=True, exist_ok=True)
            copy2(source, destination)
            print(
                [
                    ("File copied successfully from ", Text.SUCCESS),
                    (str(source), Text.HIGHLIGHT),
                    (" to ", Text.SUCCESS),
                    (str(destination), Text.HIGHLIGHT),
                ]
            )
            return True
        except PermissionError:
            print(
                "Permission denied. Check read/write permissions for source and destination.",
                Text.ERROR,
            )
            return False
        except Exception as e:
            print(f"Failed to copy file: {type(e).__name__}: {e}", Text.ERROR)
            return False


class DirectoryCopier(Copier):
    """Copier for directories with all their contents.

    Recursively copies entire directory structures while preserving the
    directory hierarchy. Prompts for confirmation if the destination already
    exists, allowing the user to abort or proceed with overwriting.

    Example:
        copier = DirectoryCopier()
        copier.copy(Path("source_dir/"), Path("dest_dir/"))
    """

    def copy(self, source: Path, destination: Path) -> bool:
        """Copy a directory with all its contents.

        Recursively copies the source directory to the destination. If the
        destination already exists, prompts the user for confirmation before
        proceeding. Uses shutil.copytree for recursive copying.

        Args:
            source: Path to the source directory.
            destination: Path where the directory should be copied to.

        Returns:
            True if the directory was copied successfully, False otherwise.
        """
        if not self._validate_source(source):
            return False

        if not source.is_dir():
            print(f"Source is not a directory: {source}", Text.ERROR)
            return False

        try:
            if destination.exists():
                if not self._prompt_overwrite(destination):
                    print("Copy aborted.", Text.WARNING)
                    return False
                rmtree(destination)

            copytree(source, destination, dirs_exist_ok=False)
            print(
                [
                    ("Directory copied successfully from ", Text.SUCCESS),
                    (str(source), Text.HIGHLIGHT),
                    (" to ", Text.SUCCESS),
                    (str(destination), Text.HIGHLIGHT),
                ]
            )
            return True
        except PermissionError:
            print(
                "Permission denied. Check read/write permissions for source and destination.",
                Text.ERROR,
            )
            return False
        except Exception as e:
            print(f"Failed to copy directory: {type(e).__name__}: {e}", Text.ERROR)
            return False

    def _prompt_overwrite(self, destination: Path) -> bool:
        """Prompt user for confirmation to overwrite existing directory.

        Args:
            destination: The path to the existing directory.

        Returns:
            True if the user enters 'y' or 'Y', False otherwise (defaults to no).
        """
        print(f"\n{destination} already exists.", Text.WARNING)
        response = input("Overwrite? [y/N]: ").strip().lower()
        return response == "y"


def copy_path(source: PathLike, destination: PathLike) -> bool:
    """Copy files or folders with their contents from one location to another.

    Automatically detects whether the source is a file or directory
    and uses the appropriate copier.

    Args:
        source: The source file or directory path.
        destination: The destination file or directory path.

    Returns:
        bool: True if successful, False otherwise.
    """
    source_path = TypeConverter.to_path(source)
    dest_path = TypeConverter.to_path(destination)

    copier: Copier

    # Determine copier based on source type
    if source_path.is_file():
        copier = FileCopier()
    elif source_path.is_dir():
        copier = DirectoryCopier()
    else:
        if not source_path.exists():
            print(f"Source path does not exist: {source_path}", Text.ERROR)
        else:
            print(
                f"Source is neither a file nor a directory: {source_path}", Text.ERROR
            )
        return False

    return copier.copy(source_path, dest_path)


__all__: list[str] = ["Copier", "FileCopier", "DirectoryCopier", "copy_path"]
