"""Base command infrastructure for CLI commands."""

from argparse import ArgumentParser, Namespace

from ..utils import ExitCode

__all__: list[str] = ["BaseCommand"]


class BaseCommand:
    """Base class for all CLI commands.

    Subclass this and implement :attr:`prog`, :attr:`help`,
    :meth:`add_arguments`, and :meth:`handle` to define a command. Invoke the
    command by calling the instance with a list of CLI arguments.

    Example::

        class GreetCommand(_BaseCommand):
            prog = "greet"
            help = "Say hello."

            def add_arguments(self, parser: ArgumentParser) -> None:
                parser.add_argument("name", help="Name to greet.")

            def handle(self, args: Namespace) -> ExitCode:
                print(f"Hello, {args.name}!")
                return ExitCode.SUCCESS

        exit_code = GreetCommand()(["Alice"])  # prints "Hello, Alice!"

    """

    prog: str = ""
    """The program name shown in usage output. Set this on the subclass."""

    help: str = ""
    """Short description of the command, used as the parser's description. Set this on the subclass."""

    epilog: str = ""
    """Optional epilog text to display after the argument help. Set this on the subclass."""

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Register arguments onto the parser.

        Called automatically by :meth:`create_parser`. Override this to add
        arguments via ``parser.add_argument(...)`` instead of defining them
        directly inside :meth:`create_parser`, keeping argument declaration
        and parser configuration separate.
        """

    def create_parser(self) -> ArgumentParser:
        """Construct and return the argument parser using :attr:`prog` and :attr:`help`.

        Called automatically by :meth:`__call__`. You should not need to
        override this in subclasses — define :attr:`prog`, :attr:`help`, and
        :meth:`add_arguments` instead.
        """
        parser = ArgumentParser(prog=self.prog, description=self.help, epilog=self.epilog)
        self.add_arguments(parser)
        return parser

    def handle(self, args: Namespace) -> ExitCode:
        """Execute the command logic with the parsed arguments.

        Receives the :class:`~argparse.Namespace` produced by parsing argv
        and should return :attr:`~ExitCode.SUCCESS` or :attr:`~ExitCode.ERROR`.

        Raises:
            NotImplementedError: If not overridden in a subclass.

        """
        raise NotImplementedError

    def __call__(self, argv: list[str]) -> ExitCode:
        """Parse ``argv`` and run the command.

        This is the primary entry point. Instantiate the command and call it
        directly with the raw argument list, typically sourced from
        ``sys.argv[1:]`` or a router that dispatches subcommands.

        Example::

            exit_code = MyCommand()(sys.argv[1:])

        """
        return self.handle(self.create_parser().parse_args(argv))
