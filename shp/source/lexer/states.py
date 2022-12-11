"""
Static HTML Preprocessor
Jakub21, 2022 Q4
--------------------------------
Lexer states
"""

__all__ = ['StateReady', 'StateDone']


class LexerState:
  def __init__(self, lexer):
    self.lexer = lexer


class StateReady(LexerState):
  def __init__(self, lexer):
    super().__init__(lexer)


class StateDone(LexerState):
  def __init__(self, lexer):
    super().__init__(lexer)
