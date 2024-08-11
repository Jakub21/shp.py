"""
Static HTML Preprocessor
Jakub21, 2023 Q2
--------------------------------
Implementation of a lang function.
"""

from ...common import resolve_path
from ..base.lang_function import LangFunction


class Include(LangFunction):
    def __init__(self, *args):
        super().__init__(*args)
        self.target = None  # Target dependency this statement points to

    def at_traverse(self):
        path = self.node.attributes.file[-1]
        self.target = self.dependency.add_dependency_path(resolve_path(self.dependency, path))

    def at_extend(self):
        self.node.replace_with(*self.target.tree.children)

    def at_define(self):
        pass

    def at_finalize(self):
        pass
