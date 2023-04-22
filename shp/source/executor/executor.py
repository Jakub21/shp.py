"""
Static HTML Preprocessor
Jakub21, 2023 Q2
--------------------------------
Executor class handles all function calls in the dependency tree.
"""

from .functions import store


class Executor:
  def __init__(self):
    self.func_calls = []

  def add_nodes(self, dependency, nodes):
    for node in nodes:
      self.func_calls.append(store[node.tag](dependency, node))

  def launch_stage(self, stage_name, *args):
    for call in self.func_calls:
      call.run_stage(stage_name, *args)
