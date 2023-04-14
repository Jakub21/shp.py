"""
Static HTML Preprocessor
Jakub21, 2022 Q4
--------------------------------
Document node class.
"""

__all__ = ['Node']

from ...position import Position


class Node:
  def __init__(self):
    self.children = []
    self.type_ = ''
    self.tag = ''
    self.content = ''
    self.attributes = {}
    self.depth = 0
    self.parent = None
    self.position = None  # position.copy() if position is not None else None

  def __str__(self):
    attrs = ' '.join([f'{k}:{v}' for k, v in self.attributes.items()])
    return f'<{self.tag} ({self.type_}) "{self.shortContent()}" {attrs}>'

  def treeRepr(self, indent='    '):
    result = f'{indent * self.depth}{self}'
    if not len(self.children):
      return result + '\n'
    result += ' {\n'
    result += ''.join([c.treeRepr(indent) for c in self.children])
    result += f'{indent * self.depth}}}\n'
    return result

  def appendNode(self, node):
    self.children += [node]
    node.depth = self.depth + 1
    node.parent = self

  def addAttribute(self, key, value):
    if key not in self.attributes.keys():
      self.attributes[key] = []
    self.attributes[key] += [value]

  def shortContent(self):
    content = self.content.strip().replace('\n', ' ').replace('\t', ' ')
    while '  ' in content:
      content = content.replace('  ', ' ')
    return content

  @classmethod
  def Root(cls):
    """Creates tree-root node"""
    obj = cls()
    obj.tag = 'root'
    obj.type_ = 'Root'
    return obj

  @classmethod
  def Normal(cls, position, tag):
    """Creates a regular node that represents a HTML tag"""
    obj = cls()
    obj.position = position.copy() if position is not None else None
    obj.tag = tag
    obj.type_ = 'Tag'
    return obj

  @classmethod
  def Preform(cls, position, tag):
    """Creates a regular node that represents a HTML tag with preformatted content"""
    obj = cls()
    obj.position = position.copy() if position is not None else None
    obj.tag = tag
    obj.type_ = 'Pref'
    return obj

  @classmethod
  def Function(cls, position, tag):
    """Creates a regular node that represents a SHP function call"""
    obj = cls()
    obj.position = position.copy() if position is not None else None
    obj.tag = tag
    obj.type_ = 'Func'
    return obj

  @classmethod
  def Content(cls, position, content):
    """Creates a regular node that represents a piece of non-tag content"""
    obj = cls()
    obj.position = position.copy() if position is not None else None
    obj.content = content
    obj.type_ = 'Content'
    return obj

  @classmethod
  def FromToken(cls, token):
    """Creates a node based on a token"""
    func, args = {
      'Tag': (cls.Normal, (token.position, token.noprefix)),
      'TagPre': (cls.Preform, (token.position, token.noprefix)),
      'TagFunc': (cls.Function, (token.position, token.noprefix)),
      'Text': (cls.Content, (token.position, token.fullData)),
    }[token.type_]
    return func(*args)
