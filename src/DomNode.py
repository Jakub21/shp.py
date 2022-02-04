from Namespace import Namespace

class DomNode(Namespace):
  def __init__(self, tag=None, scopeless=False):
    self.tag = tag
    self.parameters = Namespace()
    self.children = []
    self.scopeless = scopeless
    self.isText = False
    self.isDoctype = False
    self.isFunction = False
    self.parent = None # set when added to DOM
    self.depth = 0 # set when added to DOM

  def addParameter(self, key, value):
    self.parameters[key] = value

  def appendChild(self, child):
    self.children.append(child)
    child.parent = self
    child.depth = self.depth +1

  def insertChild(self, child, index):
    self.children.insert(index, child)
    child.parent = self
    child.depth = self.depth +1

  def appendText(self, text):
    try: lastNodeTag = self.children[-1].tag
    except IndexError: lastNodeTag = None
    if lastNodeTag == '__text__':
      self.children[-1].text += ' ' + text
    else:
      self.appendChild(DomNodeText(text))

  def duplicate(self, newParent=None):
    other = DomNode(self.tag, self.scopeless)
    other.isText = self.isText
    other.isFunction = self.isFunction
    other.parameters = Namespace(**{k:v for k,v in self.parameters.items()})
    for child in self.children:
      child.duplicate(other)
    if newParent is not None:
      newParent.appendChild(other)
    return other

  def recalcSubtreeDepths(self):
    for child in self.children:
      child.depth = self.depth +1
      child.recalcSubtreeDepths()

  def __str__(self):
    indent = self.depth * '  '
    if self.isText: return f'{indent}"{self.text}"'
    result = f'{indent}<{self.tag}{"/" if self.scopeless else ""}>'
    if len(self.children):
      result += ' {\n'
      for child in self.children:
        result += str(child)
      result += f'\n{indent}}}\n'
    return result


class DomNodeText(DomNode):
  def __init__(self, text):
    super().__init__('__text__')
    self.text = text
    self.isText = True
    self.scopeless = True

  def duplicate(self, newParent):
    other = super().duplicate(newParent)
    other.text = self.text
    return other


class DoctypeNode(DomNode):
  def __init__(self):
    super().__init__('__doctype__')
    self.isDoctype = True
    self.scopeless = True
