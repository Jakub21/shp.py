from shp.func.Function import Function

class FuncDefine(Function):
  name = 'define'
  forceBefore = ['paste', 'namespace']

  def execute(self):
    ns = self.getNamespace()
    try:
      id = self.node.params.id
    except AttributeError:
      raise ShpFunctionParamNotFoundError(self.name, 'id').setCall(self)
    self.source.compiler.addDefinition(ns + [id], self.node.children)
    self.node.removeSelf()
