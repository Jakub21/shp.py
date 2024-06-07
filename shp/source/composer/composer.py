"""
Static HTML Preprocessor
Jakub21, 2023 Q2
--------------------------------
Composer class for building / composing output files
"""

from .rules import *
from ..common import HTML_BUILD

"""
Composer phases
OPEN 1st rules run when node is opened
CLOSE 2nd rules run after the children and content is added
"""


class Composer:
  def __init__(self, tree):
    self.tree = tree
    self.current = None
    self.rules = []
    self.result = HTML_BUILD.FilePrefix
    RuleTagName(self)
    RuleAttributes(self)
    RuleAppendContent(self)

  def compose(self, node=None):
    for child in self.tree.children:
      self._compose_node(child)
    self.result += HTML_BUILD.FileSuffix
    return self.result

  def _compose_node(self, node):
    self._run_rules(node, 'open')
    for child in node.children:
      self._compose_node(child)
    self._run_rules(node, 'close')

  def _run_rules(self, node, phase):
    self.current = node
    for rule in self.rules:
      portion = getattr(rule, f'run_{phase}')()
      self.result += portion or ''
