from src.Token import Token, Position
from src.Settings import LangData
from src.LexerState import LexerStateNormal

class Lexer:
  def __init__(self):
    self.reset()

  def reset(self):
    self.tokens = []
    self.currentToken = Token('', [0,0])
    self.state = LexerStateNormal(self)

  def tokenize(self, text):
    self.reset()
    lines = text.split('\n')
    for lineNo, line in enumerate(lines):
      line += '\n' # for comment end detection
      for charNo in range(len(line)):
        self.state.tokenize(line, Position(lineNo, charNo))
