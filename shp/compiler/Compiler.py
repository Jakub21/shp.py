from shp.compiler.RootSource import RootSource
from shp.compiler.Source import Source
from shp.compiler.LangFuncsManager import LangFuncsManager
from shp.builder.Builder import Builder
import os

class Compiler:
  def __init__(self, entryPoint):
    self.root = RootSource(entryPoint)
    self.funcs = LangFuncsManager(self)
    self.reset()

  def reset(self):
    self.funcs.reset()
    self.includedFiles = []

  def compile(self):
    self.reset()
    self.root.parse()
    self._compile(self.root)
    tree = self.root.root
    tree.updateDepth(-1)
    self.funcs.executeTree(tree)
    return Builder().build(tree)

  def _compile(self, source):
    subSources = self.resolveDeps(source)
    for sub in subSources:
      self.includedFiles += [sub.path]
      sub.parse()
      self._compile(sub)
    source.resolve(subSources)

  def resolveDeps(self, source):
    sources = []
    for dep in source.deps:
      sources.append(Source.fromDependency(dep))
    return sources
