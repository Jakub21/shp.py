"""
Static HTML Preprocessor
Jakub21, 2023 Q2
--------------------------------
Traverser class for searching for nodes in the tree.
"""


class Traverser:
  def __init__(self, tree):
    self.tree = tree

  def find_all(self, callback, nodes=None):
    nodes = nodes or [self.tree]
    result = []
    for node in nodes:
      if callback(node):
        result.append(node)
      if node.children:
        result += self.find_all(callback, node.children)
    return result
