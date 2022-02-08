from shp.compiler.ShpDefinitions import ShpDefinitions

class Dependency:
  def __init__(self, source, includeNode):
    self.source = source
    self.file = self.sanitize(includeNode.params.file)
    self.includeNode = includeNode

  def __str__(self):
    return f'<Dependency "{self.file}" from "{self.source.path}" {self.includeNode.pos}>'

  @staticmethod
  def sanitize(path):
    return path.replace(' ', '')\
      .replace(ShpDefinitions.Literal, '')
