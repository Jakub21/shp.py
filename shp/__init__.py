"""
Static HTML Preprocessor
Jakub21, 2022 Q4
--------------------------------
__init__
"""

__all__ = ["Compiler", "Dependency", "Lexer", "Parser", "ROOT"]

from pathlib import Path

from .source import Compiler, Dependency, Lexer, Parser

ROOT = Path(__file__).parent
