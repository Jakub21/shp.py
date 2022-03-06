from shp.errors import *
from shp.func.Function import Function

class FuncPaste(Function):
  name = 'paste'
  forceBefore = ['namespace']

  def execute(self):
    ns = self.getNamespace()
    try:
      scope = self.node.params['from'].split('/')
    except KeyError:
      scope = []
    try:
      id = self.node.params.id
    except AttributeError:
      raise ShpFunctionParamNotFoundError(self.name, 'id')
    path = ns + scope + [id]
    nodes = self.source.compiler.getDefinition(path)
    self.node.replaceSelfList(nodes)
