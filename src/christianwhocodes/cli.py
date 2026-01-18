from argparse import ArgumentParser
from sys import exit
from typing import NoReturn

from christianwhocodes.generators.file import (
    FileGenerator,
    FileGeneratorOption,
    PgPassFileGenerator,
    PgServiceFileGenerator,
    SSHConfigFileGenerator,
)
from christianwhocodes.utils import (
    ExitCode,
    PlatformInfo,
    Version,
    generate_random_string,
    print,
)


def create_parser() -> ArgumentParser:
    parser = ArgumentParser(
        prog="christianwhocodes",
        description="Christian Who Codes CLI Tool",
        epilog="...but the people who know their God shall be strong, and carry out great exploits. [purple]—[/] [bold green]Daniel[/] 11:32",
    )

    # Add version argument
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=Version.get("christianwhocodes")[0],
        help="Show program version",
    )

    # Add platform argument
    parser.add_argument(
        "-p",
        "--platform",
        action="store_true",
        help="Show platform and architecture information",
    )

    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Random string generator subcommand
    random_parser = subparsers.add_parser(
        "random",
        aliases=["generaterandom", "randomstring"],
        help="Generate a random string",
    )
    random_parser.add_argument(
        "--no-clipboard", action="store_true", help="Don't copy the result to clipboard"
    )
    random_parser.add_argument(
        "-l",
        "--length",
        type=int,
        default=16,
        help="Length of the random string (default: 16)",
    )

    # File generator subcommand
    generate_parser = subparsers.add_parser(
        "generate",
        help=f"Generate configuration files ({', '.join(o.value for o in FileGeneratorOption)})",
    )
    generate_parser.add_argument(
        "-f",
        "--file",
        choices=[opt.value for opt in FileGeneratorOption],
        required=True,
        type=FileGeneratorOption,
        help=f"Which file to generate (options: {', '.join(o.value for o in FileGeneratorOption)}).",
    )
    generate_parser.add_argument(
        "--force",
        action="store_true",
        help="Force overwrite without confirmation",
    )

    return parser


def main() -> NoReturn:
    """Main entry point for the CLI.

    Parses command-line arguments and dispatches to appropriate handlers.
    Exits with appropriate exit code after execution.
    """
    parser = create_parser()
    args = parser.parse_args()

    # Handle platform flag
    if args.platform:
        platform_info = PlatformInfo()
        print(f"[bold cyan]Platform:[/] {platform_info.os_name}")
        print(f"[bold cyan]Architecture:[/] {platform_info.architecture}")
        print(f"[bold cyan]Full:[/] {platform_info}")
    else:
        match args.command:
            case "random" | "generaterandom" | "randomstring":
                generate_random_string(
                    length=args.length, no_clipboard=args.no_clipboard
                )

            case "generate":
                generators: dict[FileGeneratorOption, type[FileGenerator]] = {
                    FileGeneratorOption.PG_SERVICE: PgServiceFileGenerator,
                    FileGeneratorOption.PGPASS: PgPassFileGenerator,
                    FileGeneratorOption.SSH_CONFIG: SSHConfigFileGenerator,
                }

                generator_class: type[FileGenerator] = generators[args.file]
                generator: FileGenerator = generator_class()
                generator.create(force=args.force)

            case _:
                print(
                    "...but the people who know their God shall be strong, and carry out great exploits. [purple]—[/] [bold green]Daniel[/] 11:32"
                )

    exit(ExitCode.SUCCESS)


if __name__ == "__main__":
    main()
