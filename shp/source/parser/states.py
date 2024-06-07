"""
Static HTML Preprocessor
Jakub21, 2022 Q4
--------------------------------
Parser states
"""

__all__ = ['getState', 'StateDefault']

from enum import Enum, auto

from namespace import Namespace

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
    for rule in self.rules:
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

  class Phases:
    KEY = 0
    EQUALS = 1
    VALUE = 2

  def __init__(self, parser):
    super().__init__(parser)
    RuleAttrsQuickID(self)
    RuleAttrsQuickClass(self)
    RuleAttrsQuickFlag(self)
    RuleExitNodeAttrs(self)
    RuleAttrsKeyValCycle(self)
    self.phase = 0
    self.current_key = ''

  def next_phase(self):
    self.phase = (self.phase + 1) % 3


# class StatePreformatted(ParserState):
#   def __init__(self, parser):
#     super().__init__(parser)
#     RuleExitPreformatted(self)
#     RuleAppendContent(self)
