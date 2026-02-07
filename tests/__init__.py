"""Test suite for the christianwhocodes package.

How to run tests
================

All tests use pytest. Make sure dev dependencies are installed first::

    uv sync                       # install all dependencies (including dev group)

Then run the full suite with::

    uv run pytest                 # run all tests
    uv run pytest -v              # verbose — shows each test name
    uv run pytest tests/test_math.py          # run a single file
    uv run pytest -k "test_prime"             # run tests matching a keyword
    uv run pytest --tb=short                  # shorter tracebacks on failure

Test organization
=================

Each test file maps to a source module:

- test_math.py       → christianwhocodes.core.math
- test_strings.py    → christianwhocodes.core.strings
- test_urls.py       → christianwhocodes.core.urls
- test_converters.py → christianwhocodes.core.converters
- test_config.py     → christianwhocodes.core.config
- test_version.py    → christianwhocodes.core.version
- test_platform.py   → christianwhocodes.core.platform
- test_enums.py      → christianwhocodes.core.enums

Tests are grouped into classes (one per function or class under test) with
descriptive method names. Each class tests:
1. Happy-path behavior with typical inputs
2. Edge cases (zero, empty, boundary values)
3. Error handling (ValueError, KeyError, etc.)
"""
