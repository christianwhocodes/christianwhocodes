"""Core utilities and types for the christianwhocodes package.

This subpackage consolidates all foundational utilities and re-exports
them via wildcard imports for convenient access from the parent package.

Modules:
    config: PyProject — pyproject.toml parser with property-based access.
    converters: TypeConverter — static methods for bool, list, and Path conversions.
    enums: ExitCode — SUCCESS/ERROR integer codes for CLI return values.
    math: Number theory helpers (primes, factorials, fibonacci, GCD, LCM, etc.).
    platform: Platform — cross-platform OS and architecture detection.
    strings: Random string generation and CLI formatting utilities.
    urls: URL path normalization (leading/trailing slashes).
    version: Version lookup via importlib.metadata with VersionResult NamedTuple.
"""

from .config import *
from .converters import *
from .enums import *
from .math import *
from .platform import *
from .strings import *
from .urls import *
from .version import *
