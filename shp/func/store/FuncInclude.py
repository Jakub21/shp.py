from os import path as op
from shp.errors import *
from shp.func.Function import Function
from shp.parser.Nodes import NodeFunction
from shp.lexer.SHPDEF import SHPDEF

class FuncInclude(Function):
  name = 'include'
  enablePreDep = True
  forceBefore = ['define', 'paste', 'namespace']

  def preDep(self):
    from shp.compiler.Source import Source
    try: path = self.node.params.file.replace(SHPDEF.Literal, '')
    except AttributeError:
      raise ShpFunctionParamNotFoundError(self.name, 'file')
    path = op.join(op.abspath(op.dirname(self.source.path)), path + '.shp')
    path = self.source._sanitizePath(path)
    self.dep = Source(self.source.compiler, path)
    self.source.addDependency(self.dep)

  def execute(self):
    nsNode = NodeFunction('namespace', self.node.pos)
    nsNode.children = self.dep.treeRoot.children
    nsNode.params._from_include_ = self.node.params.file
    for child in nsNode.children:
      child.parent = nsNode
    try: nsNode.params.id = self.node.params['as']
    except KeyError: pass
    self.node.replaceSelf(nsNode)
    self.source.injectFuncNode(nsNode)
