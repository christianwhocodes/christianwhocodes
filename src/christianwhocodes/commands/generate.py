"""Configuration file generation command."""

from argparse import Namespace

from ..core.enums import ExitCode


def handle_file_generation(args: Namespace) -> ExitCode:
    """Generate configuration files from templates.

    Creates common developer configuration files (PostgreSQL, SSH) in their
    standard locations with template content.

    Args:
        args: Parsed arguments containing:
            - file (FileGeneratorOption): Type of file to generate
            - force (bool): Whether to overwrite without confirmation

    Returns:
        ExitCode.SUCCESS after generating the file.

    Example:
        $ christianwhocodes generate -f pgpass

        File written to /home/user/.pgpass
        Permissions set to 600 for /home/user/.pgpass

    """
    from ..generators.base import FileGenerator, FileGeneratorOption
    from ..generators.configs import (
        PgPassFileGenerator,
        PgServiceFileGenerator,
        SSHConfigFileGenerator,
    )

    # Map file generator options to their corresponding classes
    generators: dict[FileGeneratorOption, type[FileGenerator]] = {
        FileGeneratorOption.PG_SERVICE: PgServiceFileGenerator,
        FileGeneratorOption.PGPASS: PgPassFileGenerator,
        FileGeneratorOption.SSH_CONFIG: SSHConfigFileGenerator,
    }

    generator_class: type[FileGenerator] = generators[args.file]
    generator: FileGenerator = generator_class()
    success = generator.create(force=args.force)
    return ExitCode.SUCCESS if success else ExitCode.ERROR


__all__: list[str] = ["handle_file_generation"]
