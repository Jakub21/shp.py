from Namespace import Namespace
from src.compiler.LangFuncsDefinitions import definitions

class Call:
  def __init__(self, node):
    self.node = node
    self.func = definitions[self.node.tagName]
    self.ns = self.traverseForNs()

  def __str__(self):
    return f'<Call {self.node.tagName} {self.node.pos}>'

  def execute(self, manager):
    self.func(manager, self)

  def traverseForNs(self):
    ns = []
    node = self.node.parent
    while node is not None:
      if node.tagName == 'namespace':
        ns = [node.params.id] + ns
      node = node.parent
    return ns


class LangFuncsManager:
  def __init__(self, compiler):
    self.compiler = compiler
    self.forcedExecOrder = ['define', 'paste', 'namespace']
    self.reset()

  def reset(self):
    self.defs = []
    self.calls = []

  def executeTree(self, tree):
    self.calls = self.findAllCalls(tree)
    self.sortForcedCalls()
    for call in self.calls:
      call.execute(self)

  def findAllCalls(self, tree):
    calls = []
    for child in tree.children:
      if child.isType('Function'):
        calls.append(Call(child))
      if child.isType('Scoped'):
        calls += self.findAllCalls(child)
    return calls

  def sortForcedCalls(self):
    order = self.forcedExecOrder
    newOrder = []
    for name in order:
      newOrder += list(filter(lambda c: c.node.tagName == name, self.calls))
    for call in self.calls:
      if call not in newOrder: newOrder.append(call)
    self.calls = newOrder
