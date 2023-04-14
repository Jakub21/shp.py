"""
Static HTML Preprocessor
Jakub21, 2022 Q4
--------------------------------
Lexer base class. Converts raw text to a list of tokens.
"""

__all__ = ['Lexer']

from ..errors import LexerError
from .states import getState, StateDefault, StateLiteral
from .token import Token
from ..position import Position


class Lexer:
  def __init__(self):
    self.state = None # current state
    self.data = None # data fed to the lexer
    self.tokens = None # list of tokens
    self.position = None # pointer to the current position
    self.currentToken = None # currently edited token
    self.reset()

  def reset(self):
    self.state = StateDefault(self)
    self.tokens = []
    self.position = Position(0, 0)
    self.currentToken = Token()

  def feed(self, data):
    self.data = data
    self.position = Position(0, 0)

  def tokenize(self):
    for char in self.data:
      self.state.tokenize()
      self.position.advance(char)
    self.validate()

  def validate(self):
    # TODO: Make an actual validator
    if isinstance(self.state, StateLiteral):
      raise LexerError('Unexpected end of data: A literal string was not closed')

  def changeState(self, name):
    self.state = getState(name)(self, self.state)

  def previousState(self):
    self.state = self.state.spawnedFrom

  def nextToken(self, data=''):
    if not self.currentToken.isNull():
      self.tokens.append(self.currentToken)
    self.currentToken = Token(data, self.position.copy())

  def match(self, what):
    index = self.position.index
    return self.data[index:].startswith(what)

  def matchAny(self, what):
    return any([self.match(elm) for elm in what])

  @property
  def currentChar(self):
      return self.data[self.position.index]
