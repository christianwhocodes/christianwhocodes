"""Input/Output operations for console and filesystem.

This subpackage provides all user-facing I/O functionality:

Modules:
    console: Rich-powered styled output (print, status spinners)
             with a Text enum for semantic color theming.
    fscopy: File and directory copy operations via the Copier ABC
            (FileCopier, DirectoryCopier) and the convenience copy_path() function.
"""

from .console import *
from .fscopy import *
