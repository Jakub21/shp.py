from src.builder.BuilderStates import BuilderStateScoped

class Builder:
  def __init__(self):
    self.state = BuilderStateScoped(self)
    self.html = ''

  def build(self, tree):
    for node in tree.children:
      self.state.build(node)
    return self.html
