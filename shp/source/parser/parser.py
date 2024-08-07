"""
Static HTML Preprocessor
Jakub21, 2022 Q4
--------------------------------
Parser base class. Converts list of tokens into an abstract node tree.
"""

__all__ = ["Parser"]

from .node import Node
from .states import StateDefault, get_state


class Parser:
    def __init__(self, dependency, tokens=None):
        self.dependency = dependency  # dependency reference for error tracking
        self.state = StateDefault(self)  # current state
        self._tokens = tokens or []  # list of tokens fed to the parser
        self._index = 0  # index of the currently parsed token
        self.tree = Node.Root()  # DOM tree abstraction made of Nodes
        self.selection = self.tree  # currently selected node

    def parse(self):
        for index, token in enumerate(self._tokens):
            self._index = index
            self.state.parse()

    def change_state(self, name):
        self.state = get_state(name)(self)

    @property
    def current_token(self):
        return self._tokens[self._index]

    def select(self, node):
        self.selection = node

    def tree_repr(self, indent="    "):
        return self.tree.tree_repr(indent)
