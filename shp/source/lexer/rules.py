"""
Static HTML Preprocessor
Jakub21, 2022 Q4
--------------------------------
Individual tokenization rules used by lexer states.
"""

from ..common.LANG import LANG, WHITESPACE, TOKEN_TYPE


class LexerRule:
  def __init__(self, lexerState, isDefault=False):
    self.lexer = lexerState.lexer
    if not isDefault:
      lexerState.rules.append(self)

  def __str__(self):
    return f'<Rule {self.__class__.__name__}>'

  def run(self):
    raise NotImplementedError
    # return True to continue processing the current position
    # return False to stop


class RuleAppendChar(LexerRule):
  def run(self):
    self.lexer.currentToken.append(self.lexer.currentChar)
    return True
    # Fallback rule that always adds current char to the token


class RuleIgnore(LexerRule):
  def run(self):
    return True
    # Fallback rule that always ignores the character


class RulePrevious(LexerRule):
  def run(self):
    self.lexer.previousState()
    return True


# NOTE: Almost the same as below, could be simplified somehow
class RuleNewlineTail(LexerRule):
  def run(self):
    if self.lexer.matchAny('\n'):
      token = self.lexer.currentToken
      if token.isNull():
        token = self.lexer.tokens[-1]
      token.appendTail(self.lexer.currentChar)
    return True


class RuleWhitespaceTail(LexerRule):
  def run(self):
    if self.lexer.matchAny(WHITESPACE):
      if not self.lexer.tokens:
        return False
      token = self.lexer.currentToken
      if token.isNull():
        token = self.lexer.tokens[-1]
      token.appendTail(self.lexer.currentChar)
    return True


class RuleNextAtWhitespace(LexerRule):
  def run(self):
    if self.lexer.matchAny(WHITESPACE):
      if not self.lexer.currentToken.isNull():
        self.lexer.nextToken()
      return False
    return True


class RuleCommentChar(LexerRule):
  def run(self):
    if self.lexer.match(LANG.Comment):
      self.lexer.changeState('StateComment')
      return False
    return True


class RuleEndCommentAtNewline(LexerRule):
  def run(self):
    if self.lexer.match('\n'):
      self.lexer.previousState()
    return False


class RuleEscapeChar(LexerRule):
  def run(self):
    if self.lexer.match(LANG.Escape):
      self.lexer.changeState('StateEscape')
      return False
    return True


class RuleMarkEscaped(LexerRule):
  def run(self):
    self.lexer.currentToken.setEscaped()
    return True


class RuleLiteralEnter(LexerRule):
  def run(self):
    if self.lexer.match(LANG.Literal):
      self.lexer.currentToken.append(self.lexer.currentChar)
      self.lexer.changeState('StateLiteral')
      return False
    return True


class RuleLiteralPrevious(LexerRule):
  def run(self):
    if self.lexer.match(LANG.Literal):
      self.lexer.previousState()
      return True
    return True


class RuleNonPrefixFunctionalChar(LexerRule):
  def run(self):
    chars = [LANG.ATTR.Open, LANG.ATTR.Close, LANG.ATTR.Value,
      LANG.SCOPE.Open, LANG.SCOPE.Close]
    if self.lexer.matchAny(chars):
      self.lexer.nextToken(self.lexer.currentChar)
      self.lexer.nextToken()
      return False
    return True


class RuleFunctionalChar(LexerRule):
  def run(self):
    if self.lexer.matchAny(TOKEN_TYPE.values()):
      self.lexer.nextToken()
    return True
