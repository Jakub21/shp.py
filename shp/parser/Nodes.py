from shp.compiler.ShpDefinitions import ShpDefinitions as SHPDEF
from Namespace import Namespace

class Node:
  def __init__(self, tagName, pos):
    self.tagName = tagName
    self.pos = pos
    self.scoped = False
    self.params = Namespace()
    self.paramLiterals = []
    self.types = ['Node']
    # set when added to the tree
    self.parent = None
    self.depth = 0

  def __str__(self):
    indent = self.depth * '  '
    return f'{indent}{self.shortStr()}\n'

  def shortStr(self):
    return f'<{self.tagName} {self.pos}/>'

  def addParam(self, key, val):
    if not key in self.params.keys():
      self.params[key] = val
    else:
      self.params[key] += ' ' + val
      if key not in self.paramLiterals:
        self.paramLiterals.append(key)

  def isType(self, type):
    return type in self.types

  def updateDepth(self, depth):
    self.depth = depth


class NodeData(Node):
  def __init__(self, data, pos):
    super().__init__('__data__', pos)
    self.types.append('Data')
    self.data = data

  def __str__(self):
    indent = self.depth * '  '
    return f'{indent}{self.shortStr()}\n'

  def shortStr(self):
    return f'"{self.data}" {self.pos}'

  def appendData(self, data):
    self.data += (' ' if len(self.data) else '') + data


class NodeScoped(Node):
  def __init__(self, tagName, pos):
    super().__init__(tagName, pos)
    self.types.append('Scoped')
    self.children = []

  def __str__(self):
    indent = self.depth * '  '
    header = f'{indent}{self.shortStr()}'
    if not len(self.children):
      return f'{header}\n'
    result = f'{header} {{\n'
    for child in self.children:
      result += str(child)
    return result + f'{indent}}}\n'

  def shortStr(self):
    return f'<{self.tagName} {self.pos}>'

  def appendNode(self, node):
    self.children.append(node)
    node.parent = self
    node.depth = self.depth + 1

  def appendData(self, data, pos):
    try: self._appendDataToLastChild(data)
    except IndexError:
      lastChild = NodeData('', pos)
      self.appendNode(lastChild)
      lastChild.appendData(data)

  def _appendDataToLastChild(self, data):
    lastChild = self.children[-1]
    if not lastChild.isType('Data'): raise IndexError
    lastChild.appendData(data)

  def updateDepth(self, depth):
    self.depth = depth
    for child in self.children:
      child.updateDepth(depth+1)


class NodeFunction(NodeScoped):
  def __init__(self, tagName, pos):
    super().__init__(tagName, pos)
    self.types.append('Function')

  def shortStr(self):
    return f'@({self.tagName} {self.pos})'

  def __str__(self):
    indent = self.depth * '  '
    header = f'{indent}{self.shortStr()}'
    if not len(self.children):
      return f'{header}\n'
    result = f'{header} {{\n'
    for child in self.children:
      result += str(child)
    return result + f'{indent}}}\n'

  def removeSelf(self):
    index = self.parent.children.index(self)
    del self.parent.children[index]

  def replaceSelf(self, node):
    index = self.parent.children.index(self)
    self.parent.children[index] = node
    node.parent = self.parent
    node.updateDepth(self.depth)

  def replaceSelfList(self, nodes):
    index = self.parent.children.index(self)
    del self.parent.children[index]
    self.parent.children[index:index] = nodes
    for child in nodes:
      child.parent = self.parent
      child.updateDepth(self.depth)
