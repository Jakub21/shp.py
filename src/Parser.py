# TEMP
import traceback as tb

from src.ParserState import *
from src.DomNode import DomNode

class Parser:
  def __init__(self):
    self.reset()

  def reset(self):
    self.state = ParserStateDefault(self)
    self.dom = DomNode('DOM')
    self.dom.depth = -1
    self.currentScope = self.dom
    self.lastTag = self.dom

  def parse(self, tokens):
    self.reset()
    for token in tokens:
      self.state.parseToken(token)
