from shp.func.Function import Function

class FuncNamespace(Function):
  name = 'namespace'

  def execute(self):
    self.node.replaceSelfList(self.node.children)
