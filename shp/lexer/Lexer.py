from shp.lexer.Position import Position
from shp.lexer.Token import Token
from shp.lexer.LexerStates import LexerStateDefault

class Lexer:
  def __init__(self):
    self.reset()

  def reset(self):
    self.tokens = []
    self.currentToken = Token()
    self.state = LexerStateDefault(self)

  def tokenize(self, shp):
    self.reset()
    lines = shp.split('\n')
    for lineNo, line in enumerate(lines):
      line += '\n' # for comment end detection
      for charNo in range(len(line)):
        self.state.tokenize(line, Position(lineNo, charNo))
    return self.tokens
