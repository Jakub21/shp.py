"""
Static HTML Preprocessor
Jakub21, 2022 Q4
--------------------------------
Parser states
"""

__all__ = ['getState', 'StateDefault']

from enum import Enum, auto

from .rules import *


def getState(name):
  return eval(name) # TODO


class ParserState:
  def __init__(self, parser):
    self.parser = parser
    self.rules = []

  def __str__(self):
    return f'<ParserState {self.__class__.__name__}>'

  def parse(self):
    ind = self.parser.selection.depth * 4 * ' '
    # print(ind, self.parser.selection, '|', self.parser.currentToken, '|', self.__class__.__name__)
    for rule in self.rules:
      # print('  ', rule)
      if not rule.run():
        return


class StateDefault(ParserState):
  def __init__(self, parser):
    super().__init__(parser)
    RuleEnterNodeAttrs(self)
    RuleNewNode(self)
    RuleEnterScope(self)
    RuleExitScope(self)
    RuleAppendContent(self)


class StateTagAttrs(ParserState):

  class Phase(Enum):
    Key = auto()
    Sign = auto()
    Value = auto()

  def __init__(self, parser):
    super().__init__(parser)
    RuleAttrsQuickID(self)
    RuleAttrsQuickClass(self)
    RuleAttrsQuickFlag(self)
    RuleExitNodeAttrs(self)
    RuleAttrsKeyValCycle(self)
    self.phase = self.Phase.Key


# class StatePreformatted(ParserState):
#   def __init__(self, parser):
#     super().__init__(parser)
#     RuleExitPreformatted(self)
#     RuleAppendContent(self)
