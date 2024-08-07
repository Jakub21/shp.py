"""
Static HTML Preprocessor
Jakub21, 2023 Q2
--------------------------------
Executor class handles all function calls in the dependency tree.
"""

from namespace import Namespace

from ..common.errors import UnknownFunctionError
from .functions import store


class Executor:
    def __init__(self):
        self.func_calls = []
        self.doc_data = Namespace.Kwargs(
            slots={},
        )

    def add_nodes(self, dependency, nodes):
        for node in nodes:
            try:
                function_class = store[node.tag.lower()]
            except KeyError:
                raise UnknownFunctionError(
                    dependency, node.position, node.tag
                ) from None
            self.func_calls.append(function_class(self, dependency, node))

    def launch_stage(self, stage_name, *args):
        for call in self.func_calls:
            call.run_stage(stage_name, *args)
