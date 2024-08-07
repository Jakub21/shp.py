"""
Static HTML Preprocessor
Jakub21, 2023 Q2
--------------------------------
Dependency class stores a file reference and its dependencies.
"""

__all__ = ["Dependency"]

from ..common.errors import DependencyNotFoundError
from ..lexer import Lexer
from ..parser import Node, Parser


class Dependency:
    tree: Node
    dependencies: ["Dependency"]

    def __init__(self, path):
        self.path = path
        self.reset()

    def __repr__(self):
        return f'<Dependency "{self.path}">'

    def reset(self):
        self.tree = None
        self.dependencies = []

    def parse(self):
        try:
            with open(self.path) as file:
                content = file.read()
        except DependencyNotFoundError:
            raise DependencyNotFoundError(self) from None
        lexer = Lexer(self, content)
        lexer.tokenize()
        parser = Parser(self, lexer.tokens)
        parser.parse()
        self.tree = parser.tree

    def add_dependency(self, dep):
        self.dependencies.append(dep)

    def add_dependency_path(self, path):
        dep = self.__class__(path)
        self.add_dependency(dep)
        return dep
