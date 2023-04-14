"""
Static HTML Preprocessor
Jakub21, 2022 Q4
--------------------------------
Lexer states
"""

__all__ = ['getState', 'StateDefault', 'StateLiteral']

from .token import Token
from .rules import *


def getState(name):
  return eval(name) # TODO


class LexerState:
  def __init__(self, lexer, current=None):
    self.lexer = lexer
    self.rules = []
    self._default = RuleAppendChar(self, True)
    self.spawnedFrom = current

  def __str__(self):
    return f'<LexerState {self.__class__.__name__}>'

  def ensureValidToken(self):
    if self.lexer.currentToken.isNull():
      self.lexer.currentToken = Token('', self.lexer.position)

  def tokenize(self):
    self.ensureValidToken()
    # print(self, f'"{self.lexer.currentChar}"')
    for rule in self.rules:
      # print('  ', rule, self.lexer.currentToken)
      if not rule.run():
        # print('[break]')
        return
    self._default.run()
    # print('  ', self._default, self.lexer.currentToken)
    # print('[done]')


class StateDefault(LexerState):
  def __init__(self, lexer, current=None):
    super().__init__(lexer, current)
    RuleWhitespaceTail(self)
    RuleNextAtWhitespace(self)
    RuleEscapeChar(self)
    RuleCommentChar(self)
    RuleNonPrefixFunctionalChar(self)
    RuleLiteralEnter(self)
    RuleFunctionalChar(self)


class StateComment(LexerState):
  def __init__(self, lexer, current=None):
    super().__init__(lexer, current)
    RuleNewlineTail(self)
    RulePreviousAtNewline(self)
    self._default = RuleIgnore(self)


class StateLiteral(LexerState):
  def __init__(self, lexer, current=None):
    super().__init__(lexer, current)
    RuleWhitespaceTail(self)
    RuleEscapeChar(self)
    RuleLiteralPrevious(self)


class StateEscape(LexerState):
  def __init__(self, lexer, current=None):
    super().__init__(lexer, current)
    RuleWhitespaceTail(self)
    RulePrevious(self)
    RuleMarkEscaped(self)
