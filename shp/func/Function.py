
class Function:
  name = 'UNNAMED'
  enablePreDep = False # execute before dependencies are resolved
  forceBefore = [] # must be executed before all funcs with those names

  def __init__(self, source, node):
    self.originalSource = source
    self.source = source
    self.node = node
    self.done = False
    self.preDepDone = False

  def __str__(self):
    file = self.originalSource.path.split("/")[-1]
    return f'<@{self.name} from "{file}" at {self.node.pos}>'

  def run(self):
    self.done = True
    self.execute()

  def execute(self):
    raise TypeError(f'{self}: Function is not implemented')

  def runPreDep(self):
    self.preDepDone = True
    self.preDep()

  def preDep(self):
    raise TypeError(f'{self}: this function has no pre-dep')

  def getNamespace(self):
    ns = []
    node = self.node.parent
    while node is not None:
      if node.tagName == 'namespace':
        try: ns = [node.params.id] + ns
        except AttributeError: pass # NOTE
      node = node.parent
    return ns
