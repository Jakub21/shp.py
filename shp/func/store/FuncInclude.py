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
    realPath = self.getRealPath(path)
    self.dep = Source(self.source.compiler, realPath)
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

  def getRealPath(self, pathParam):
    if pathParam.startswith(SHPDEF.IncludePathFromRoot):
      root = self.source.compiler.entryPoint.path
      pathParam = pathParam[len(SHPDEF.IncludePathFromRoot):]
    else:
      root = self.originalSource.path
    while pathParam.startswith(SHPDEF.IncludePathBack):
      root = '/'.join(root.split('/')[:-1])
      pathParam = pathParam[len(SHPDEF.IncludePathBack):]
    directory = op.dirname(root)
    path = op.join(op.abspath(directory), pathParam + '.shp')
    path = self.source._sanitizePath(path)
    return path
