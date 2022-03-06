from Namespace import Namespace
from shp.errors import *
from shp.compiler.Source import Source
from shp.builder.Builder import Builder

class Compiler:
  def __init__(self, entryPoint):
    self.entryPoint = Source(self, entryPoint)
    self.reset()

  def reset(self):
    self.dependencies = []
    self.definitions = []
    self.entryPoint.reset()

  def compile(self):
    self.reset()
    try:
      self._compileSource(self.entryPoint)
      self._gatherDependencyCalls()
      self.entryPoint.finalize()
      self.entryPoint.treeRoot.updateDepth(0)
      html = Builder().build(self.entryPoint.treeRoot)
      return Namespace(success=True, html=html)
    except ShpError as error:
      return Namespace(success=False, error=error)

  def _compileSource(self, source):
    source.buildTree()
    source.execPreDep()
    for dep in source.dependencies:
      self._compileSource(dep)

  def _gatherDependencyCalls(self):
    for dep in self.dependencies:
      self.entryPoint.calls += dep.calls
      for call in dep.calls:
        call.source = self.entryPoint
    self.entryPoint._sortFuncCalls(self.entryPoint.calls)

  def addDependency(self, source):
    self.dependencies += [source]

  def addDefinition(self, path, content):
    if path in [d.path for d in self.definitions]:
      raise ShpDefinitionRepeatedError(path)
    self.definitions += [Namespace(path=path, content=content)]

  def getDefinition(self, path):
    for d in self.definitions:
      if d.path == path:
        return d.content
    raise ShpDefinitionNotFoundError(path)
