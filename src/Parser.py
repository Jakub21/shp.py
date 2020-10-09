from Namespace import Namespace

from src.ParserState import *
from src.DomNode import DomNode
from src.Settings import LangFunctions

class Parser:
  def __init__(self):
    self.reset()
    self.functions = LangFunctions()

  def reset(self):
    self.state = ParserStateDefault(self)
    self.definitions = Namespace()
    self.funcCalls = []
    self.dom = DomNode('DOM')
    self.dom.depth = -1
    self.currentScope = self.dom
    self.lastTag = self.dom

  def parse(self, tokens):
    self.reset()
    for token in tokens:
      self.state.parseToken(token)
    for func in self.funcCalls:
      func.execute(self)
