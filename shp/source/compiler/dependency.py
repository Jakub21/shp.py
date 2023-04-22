"""
Static HTML Preprocessor
Jakub21, 2023 Q2
--------------------------------
Dependency class stores a file reference and its dependencies.
"""

__all__ = ['Dependency']

from ..lexer import Lexer
from ..parser import Parser
from ..common.errors import ShpDependencyError


class Dependency:
  def __init__(self, path):
    self.path = path
    self.tree = None
    self.dependencies = []

  def parse(self):
    try:
      with open(self.path, 'r') as file:
        content = file.read()
    except FileNotFoundError as err:
      raise ShpDependencyError(f'File {self.path} does not exist') from None
    lexer = Lexer(content)
    lexer.tokenize()
    parser = Parser(lexer.tokens)
    parser.parse()
    self.tree = parser.tree

  def add_dependency(self, dep):
    self.dependencies.append(dep)

  def add_dependency_path(self, path):
    dep = self.__class__(path)
    self.add_dependency(dep)
    return dep
