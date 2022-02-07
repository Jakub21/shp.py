from src.lexer.Lexer import Lexer
from src.parser.Parser import Parser
from src.parser.Nodes import NodeFunction
from src.compiler.Dependency import Dependency

def sanitizePath(path):
  return path.replace('\\', '/')


class RootSource:
  def __init__(self, path):
    self.path = path
    self.root = self.parseFile(path)
    self.deps = self.traverseForDeps(self.root)

  def __str__(self):
    return f'<Source "{self.path}" (root)>'

  def parseFile(self, path):
    path = sanitizePath(path)
    with open(path, 'r') as file:
      tokens = Lexer().tokenize(file.read())
      return Parser().parse(tokens)

  def resolve(self, subSources):
    for source in subSources:
      node = source.dep.includeNode
      newNode = NodeFunction('namespace', node.pos)
      newNode.params.id = node.params['as']
      newNode.children = source.root.children
      for child in newNode.children:
        child.parent = newNode
        child.updateDepth(node.depth+1)
      node.replaceSelf(newNode)

  def traverseForDeps(self, node):
    deps = []
    if node.isType('Function') and node.tagName == 'include':
      deps.append(Dependency(self, node))
    elif node.isType('Scoped'):
      for child in node.children:
        deps += self.traverseForDeps(child)
    return deps
