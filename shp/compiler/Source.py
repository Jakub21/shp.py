from shp.compiler.RootSource import RootSource
import os

class Source(RootSource):
  def __init__(self, path, parent, dep):
    super().__init__(path)
    self.parent = parent
    self.dep = dep

  @classmethod
  def fromDependency(cls, dep):
    self = cls.__new__(cls)
    directory = os.path.abspath(os.path.dirname(dep.source.path))
    path = directory.replace('\\','/') + f'/{dep.file}.shp'
    super(cls, self).__init__(path)
    self.parent = dep.source
    self.dep = dep
    return self

  def __str__(self):
    return f'<Source "{self.path}">'
