from src.parser.ParserStates import ParserStateDefault
from src.parser.Nodes import NodeScoped
from src.lexer.Position import Position

class Parser:
  def __init__(self):
    self.reset()

  def reset(self):
    self.state = ParserStateDefault(self)
    self.root = NodeScoped('Root', Position(0,0))
    self.root.depth = -1
    self.currentScope = self.root
    self.lastAddedTag = self.root

  def parse(self, tokens):
    self.reset()
    for token in tokens:
      self.state.parse(token)
    return self.root
