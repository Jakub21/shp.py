
class BuilderState:
  def __init__(self, builder):
    self.builder = builder

  def switchState(self, state):
    self.builder.state = state(self.builder)

  def buildParameters(self, node):
    if not len(node.params.keys()): return ''
    result = ''
    for key, val in node.params.items():
      if key in node.paramLiterals:
        val = f"'{val}'"
      result += f' {key}={val}'
    return result


class BuilderStateScopeless(BuilderState):
  def build(self, node):
    if self.checkIsData(node): return
    if self.checkIsScoped(node): return
    self.builder.html += f'<{node.tagName}{self.buildParameters(node)}/>'

  def checkIsData(self, node):
    if node.tagName == '__data__':
      self.switchState(BuilderStateData)
      self.builder.state.build(node)
      return True

  def checkIsScoped(self, node):
    if node.isType('Scoped'):
      self.switchState(BuilderStateScoped)
      self.builder.state.build(node)
      return True


class BuilderStateScoped(BuilderStateScopeless):
  def build(self, node):
    if self.checkIsData(node): return
    if self.checkIsScopeless(node): return
    self.builder.html += f'<{node.tagName}{self.buildParameters(node)}>'
    for child in node.children:
      self.build(child)
    self.builder.html += f'</{node.tagName}>'

  def checkIsScopeless(self, node):
    if not node.isType('Scoped'):
      self.switchState(BuilderStateScopeless)
      self.builder.state.build(node)
      return True


class BuilderStateData(BuilderState):
  def build(self, node):
    if self.checkIsNonData(node): return
    self.builder.html += node.data

  def checkIsNonData(self, node):
    if node.tagName != '__data__':
      self.switchState(BuilderStateScoped)
      self.builder.state.build(node)
      return True
