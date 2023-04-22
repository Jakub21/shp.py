"""
Static HTML Preprocessor
Jakub21, 2023 Q2
--------------------------------
SHP lang function abstract class.
"""

from abc import ABC, abstractmethod
from namespace import Namespace


class LangFunction(ABC):
  def __init__(self, dependency, node):
    self.dependency = dependency
    self.node = node
    self.stage = Namespace.Kwargs(
      TRAVERSE = False,
      EXTEND = False,
      DEFINE = False,
      FINALIZE = False,
    )

  def __repr__(self):
    return f'<Call {self.__class__.__name__.lower()} at {self.node.position}>'

  def run_stage(self, stage_name, *args):
    if self.stage[stage_name.upper()]:
      return
    self.stage[stage_name.upper()] = True
    getattr(self, f'at_{stage_name}')(*args)

  @abstractmethod
  def at_traverse(self):
    pass

  def at_extend(self):
    pass

  @abstractmethod
  def at_define(self):
    pass

  @abstractmethod
  def at_finalize(self):
    pass
