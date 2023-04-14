"""
Static HTML Preprocessor
Jakub21, 2022 Q4
--------------------------------
Various SHP related exceptions
"""


class ShpError(Exception):
  pass


class LexerError(ShpError):
  pass


class ParserError(ShpError):
  pass
