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
  def __init__(self):
    self.state = None # current state
    self._tokens = None # list of tokens fed to the parser
    self._index = None # index of the currently parsed token
    self._tree = None # DOM tree abstraction made of Nodes
    self.selection = None # currently selected node
    self.reset()

  def reset(self):
    self.state = StateDefault(self)
    self._tokens = []
    self._index = 0
    self._tree = Node.Root()
    self.selection = self._tree

  def feed(self, tokens):
    self._tokens = tokens

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
    return self._tree.treeRepr(indent)
