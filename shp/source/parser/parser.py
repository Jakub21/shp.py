"""
Static HTML Preprocessor
Jakub21, 2022 Q4
--------------------------------
Parser base class. Converts list of tokens into an abstract node tree.
"""

__all__ = ['Parser']

from .states import getState, StateDefault
from .node import Node


class Parser:
  def __init__(self, tokens=None):
    self.state = StateDefault(self) # current state
    self._tokens = tokens or [] # list of tokens fed to the parser
    self._index = 0 # index of the currently parsed token
    self.tree = Node.Root() # DOM tree abstraction made of Nodes
    self.selection = self.tree # currently selected node

  def parse(self):
    for index, token in enumerate(self._tokens):
      self._index = index
      self.state.parse()

  def changeState(self, name):
    self.state = getState(name)(self)

  @property
  def currentToken(self):
    return self._tokens[self._index]

  def select(self, node):
    self.selection = node

  def treeRepr(self, indent='    '):
    return self.tree.treeRepr(indent)
