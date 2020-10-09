from src.DomNode import DomNode

class FunctionNode(DomNode):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.isFunction = True
    self.parent = None
    self.isNthChild = 0

  def setParent(self, node):
    self.parent = node
    self.isNthChild = len(node.children)

  def execute(self, parser):
    f = eval(f'parser.functions.{self.tag}')
    f(self, parser, self.parent)
