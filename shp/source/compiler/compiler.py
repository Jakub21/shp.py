"""
Static HTML Preprocessor
Jakub21, 2023 Q2
--------------------------------
SHP -> HTML transpiler class. Named compiler for convenience and compatibility.
Combines all transpiling steps into the full process.

entry_point must be an instance of Dependency
"""

__all__ = ['Compiler']

from .traverser import Traverser
from ..executor import Executor


class Compiler:
  def __init__(self, entry_point):
    self.entry_point = entry_point
    self.dependencies = []
    self.executor = Executor()

  def compile(self):
    self._compile_dependency(self.entry_point)
    self.executor.launch_stage('define')
    self.executor.launch_stage('finalize')

  def _compile_dependency(self, start):
    start.parse()
    self.traverse(start)
    for dependency in start.dependencies:
      self._compile_dependency(dependency)
    self.executor.launch_stage('extend')

  def traverse(self, start):
    func_nodes = Traverser(start.tree).find_all(lambda node: node.type_ == 'Func')
    self.executor.add_nodes(start, func_nodes)
    self.executor.launch_stage('traverse')
