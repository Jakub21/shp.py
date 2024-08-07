"""
Static HTML Preprocessor
Jakub21, 2023 Q2
--------------------------------
__init__
"""

from .filesystem import resolve_path
from .position import Position

__all__ = ["Position", "resolve_path"]
