"""
Static HTML Preprocessor
Jakub21, 2023 Q2
--------------------------------
SHP -> HTML transpiler class. Named compiler for convenience and compatibility.
Combines all transpiling steps into the full process.

entry_point must be an instance of Dependency
"""

__all__ = ["Compiler"]

from ..composer import Composer
from ..executor import Executor
from .traverser import Traverser


class Compiler:
    def __init__(self, entry_point):
        self.entry_point = entry_point
        self.dependencies = []
        self.executor = Executor()

    def compile(self):
        self.entry_point.reset()
        self._compile_dependency(self.entry_point)
        for stage in ["extend", "define", "finalize"]:
            self.executor.launch_stage(stage)
        composer = Composer(self.entry_point.tree)
        return composer.compose()

    def _compile_dependency(self, start):
        start.parse()
        self.traverse(start)
        for dependency in start.dependencies:
            self.dependencies += [dependency]
            self._compile_dependency(dependency)

    def traverse(self, start):
        func_nodes = Traverser(start.tree).find_all(lambda node: node.type_ == "Func")
        self.executor.add_nodes(start, func_nodes)
        self.executor.launch_stage("traverse")
