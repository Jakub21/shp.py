from src.compiler.RootSource import RootSource
from src.compiler.Source import Source
from src.compiler.LangFuncsManager import LangFuncsManager
from src.builder.Builder import Builder
import os

class Compiler:
  def __init__(self, entryPoint):
    self.root = RootSource(entryPoint)
    self.funcs = LangFuncsManager(self)

  def compile(self):
    self._compile(self.root)
    tree = self.root.root
    tree.updateDepth(-1)
    self.funcs.executeTree(tree)
    return Builder().build(tree)

  def _compile(self, source):
    subSources = self.resolveDeps(source)
    for sub in subSources:
      sub.parse()
      self._compile(sub)
    source.resolve(subSources)

  def resolveDeps(self, source):
    sources = []
    for dep in source.deps:
      sources.append(Source.fromDependency(dep))
    return sources
