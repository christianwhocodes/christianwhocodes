"""Christian Who Codes - Python utilities for developers.

This package provides a collection of utilities and CLI tools for common
developer tasks including file generation, string manipulation, and system
information.

The package is organized into semantic modules:
- core: Core utilities (version, platform, types, strings, math)
- io: Input/output operations (console, filesystem)
- generators: Configuration file generators
- commands: CLI command implementations
- cli: Main CLI entry point
"""

# Re-export commonly used items for convenience
from .core import (
    ExitCode,
    Platform,
    PyProject,
    TypeConverter,
    Version,
    fibonacci,
    fibonacci_sequence,
    gcd,
    generate_random_string,
    is_even,
    is_factorial,
    is_odd,
    is_perfect_square,
    is_power_of_two,
    is_prime,
    lcm,
    max_length_from_choices,
    normalize_url_path,
    print_version,
)
from .generators import (
    FileGenerator,
    FileGeneratorOption,
    PgPassFileGenerator,
    PgServiceFileGenerator,
    SSHConfigFileGenerator,
)
from .io import Text, copy_path, print

__all__ = [
    # Core utilities
    "ExitCode",
    "Platform",
    "PyProject",
    "TypeConverter",
    "Version",
    "generate_random_string",
    "max_length_from_choices",
    "normalize_url_path",
    "print_version",
    # Math utilities
    "is_prime",
    "is_factorial",
    "gcd",
    "lcm",
    "fibonacci",
    "fibonacci_sequence",
    "is_perfect_square",
    "is_even",
    "is_odd",
    "is_power_of_two",
    # Generators
    "FileGenerator",
    "FileGeneratorOption",
    "PgPassFileGenerator",
    "PgServiceFileGenerator",
    "SSHConfigFileGenerator",
    # I/O
    "Text",
    "copy_path",
    "print",
]
