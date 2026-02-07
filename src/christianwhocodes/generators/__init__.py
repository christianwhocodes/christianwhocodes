"""File generation utilities for developer configuration files.

This subpackage implements the Template Method pattern for creating
configuration files with optional overwrite confirmation.

Modules:
    base: FileGenerator ABC (template method) and FileGeneratorOption enum.
    configs: Concrete generators for PostgreSQL (.pg_service.conf, .pgpass/pgpass.conf)
             and SSH (~/.ssh/config) configuration files.
"""

from .base import *  # noqa: F403
from .configs import *  # noqa: F403
