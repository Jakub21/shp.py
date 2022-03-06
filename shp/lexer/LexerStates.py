from shp.lexer.Position import Position
from shp.lexer.Token import Token
from shp.lexer.SHPDEF import SHPDEF

class LexerState:
  def __init__(self, lexer):
    self.lexer = lexer
    self.structural = [SHPDEF.TagOpen, SHPDEF.TagClose,
      SHPDEF.ScopeOpen, SHPDEF.ScopeClose]
    self.whitespace = list(' \r\n\t')

  def switchState(self, other):
    self.lexer.state = other(self.lexer)

  def nextToken(self, pos):
    self.lexer.tokens.append(self.lexer.currentToken)
    self.lexer.currentToken = Token('', pos)
    return self.lexer.currentToken

  def checkPosMatch(self, line, pos, compare):
    if type(compare) == str:
      return line[pos.char:].startswith(compare)
    else:
      return True in [self.checkPosMatch(line, pos, entry)
        for entry in compare]


class LexerStateDefault(LexerState):
  def tokenize(self, line, pos):
    self.lexer.currentToken.initalize(pos)
    if self.checkWhitespace(line, pos): return
    if self.checkIsComment(line, pos): return
    if self.checkStructural(line, pos): return
    self.checkIsLiteral(line, pos)
    self.lexer.currentToken.append(line[pos.char])

  def checkIsComment(self, line, pos):
    if self.checkPosMatch(line, pos, SHPDEF.Comment):
      self.switchState(LexerStateComment)
      return True

  def checkIsLiteral(self, line, pos):
    if self.checkPosMatch(line, pos, SHPDEF.Literal):
      self.switchState(LexerStateLiteral)
      return True

  def checkStructural(self, line, pos):
    token = self.lexer.currentToken
    if self.checkPosMatch(line, pos, self.structural):
      if not token.isEmpty():
        token = self.nextToken(pos)
      token.append(line[pos.char])
      token = self.nextToken(pos)
      return True

  def checkWhitespace(self, line, pos):
    token = self.lexer.currentToken
    if self.checkPosMatch(line, pos, self.whitespace):
      if not token.isEmpty():
        token = self.nextToken(pos)
      return True


class LexerStateComment(LexerState):
  def tokenize(self, line, pos):
    if self.checkPosMatch(line, pos, '\n'):
      self.switchState(LexerStateDefault)


class LexerStateLiteral(LexerState):
  def tokenize(self, line, pos):
    token = self.lexer.currentToken
    token.append(line[pos.char])
    if self.checkPosMatch(line, pos, SHPDEF.Literal):
      self.nextToken(pos)
      self.switchState(LexerStateDefault)
