from Namespace import Namespace
from src.Token import Token, Position
from src.Settings import LangData

class LexerState:
  def __init__(self, lexer):
    self.lexer = lexer
    ld = LangData
    self.charsets = Namespace(
      structural = [ld.TagOpen, ld.TagClose, ld.ScopeOpen, ld.ScopeClose],
      # prefixes = [ld.TagNameScoped, ld.TagNameScopeless, ld.TagId,
      #   ld.TagClose, ld.TagFlagParam, ld.FunctionName], # unused for now
      whitespace = list(' \t\r\n')
    )
  def apply(self):
    self.lexer.tokens.append(self.lexer.currentToken)
    self.lexer.currentToken = Token('', Position(0, 0))
  def lcheck(self, line, pos, what):
    return line[pos.char:].startswith(what)
  def lcheckCategory(self, line, pos, name):
    result = False
    try: chars = self.charsets[name]
    except KeyError:
      raise KeyError(f'Undefined character category "{name}"') from None
    for c in chars:
      result = self.lcheck(line, pos, c) or result
      if result: break
    return result

class LexerStateNormal(LexerState):
  def tokenize(self, line, pos):
    if self.lexer.currentToken.isEmpty():
      self.lexer.currentToken.setPos(pos)
    if self.lcheck(line, pos, LangData.Comment):
      self.lexer.state = LexerStateComment(self.lexer)
      return
    if self.lcheck(line, pos, LangData.Literal):
      self.lexer.state = LexerStateLiteral(self.lexer)
    if self.lcheckCategory(line, pos, 'structural'):
      if not self.lexer.currentToken.isEmpty(): self.apply()
      self.lexer.currentToken.setPos(pos)
      self.lexer.currentToken.append(line[pos.char])
      self.apply()
    elif self.lcheckCategory(line, pos, 'whitespace'):
      if not self.lexer.currentToken.isEmpty():
        self.apply()
    else:
      self.lexer.currentToken.append(line[pos.char])

class LexerStateLiteral(LexerState):
  def tokenize(self, line, pos):
    self.lexer.currentToken.append(line[pos.char])
    if self.lcheck(line, pos, LangData.Literal):
      self.apply()
      self.lexer.state = LexerStateNormal(self.lexer)

class LexerStateComment(LexerState):
  def tokenize(self, line, pos):
    if self.lcheck(line, pos, '\n'):
      self.lexer.state = LexerStateNormal(self.lexer)
