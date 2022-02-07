
class Definition:
  def __init__(self, call):
    self.id = call.node.params.id
    self.ns = '/'.join(call.ns)
    self.children = call.node.children

  def __str__(self):
    if len(self.ns):
      return f'<Definition {self.id} in "{self.ns}">'
    else:
      return f'<Definition {self.id}>'
