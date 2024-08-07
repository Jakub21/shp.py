"""
Static HTML Preprocessor
Jakub21, 2023 Q2
--------------------------------
SHP lang function abstract class.
"""

from abc import ABC, abstractmethod

from namespace import Namespace


class LangFunction(ABC):
    def __init__(self, executor, dependency, node):
        self.executor = executor
        self.dependency = dependency
        self.node = node
        self.stage = Namespace.Kwargs(
            TRAVERSE=False,  # executed when the compiler searches for all function calls in the document
            EXTEND=False,  # executed to merge all dependencies into one tree
            DEFINE=False,  # priority execution on full tree
            FINALIZE=False,  # secondary execution on full tree
        )

    def __repr__(self):
        return f"<Call {self.__class__.__name__.lower()} at {self.node.position}>"

    def run_stage(self, stage_name, *args):
        if self.stage[stage_name.upper()]:
            return
        self.stage[stage_name.upper()] = True
        getattr(self, f"at_{stage_name}")(*args)

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
