"""
Static HTML Preprocessor
Jakub21, 2022 Q4
--------------------------------
Position class to identify a line and column. Both lines and columns are
0-indexed but the class representation is 1-indexed.
"""


class Position:
  def __init__(self, line=0, column=0):
    self.index = 0
    self.line = line
    self.column = column

  def __str__(self):
    return f'[{self.line+1}:{self.column+1}]'

  def copy(self):
    p = Position(self.line, self.column)
    p.index = self.index
    return p

  def _next(self):
    self.column += 1

  def _newline(self):
    self.column = 0
    self.line += 1

  def advance(self, char):
    self.index += 1
    if char == '\n':
      self._newline()
    else:
      self._next()
