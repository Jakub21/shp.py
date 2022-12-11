"""
Static HTML Preprocessor
Jakub21, 2022 Q4
--------------------------------
Lexer base class
"""

from .states import StateReady, StateDone
from .token import Token


class Lexer:
  def __init__(self):
    self._tokens = []
    self._current_token = Token()
    self._state = StateReady(self)

  def tokenize(self, inp):
    self._state = StateDone(self)
