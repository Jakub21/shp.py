from src.Settings import LangData
from Namespace import Namespace

class DomNode(Namespace):
  def __init__(self, tag=None, scopeless=True):
    self.tag = tag
    self.parameters = {}
    self.children = []
    self.scopeless = scopeless
    self.isText = False
    self.parent = None # set when added to DOM
    self.depth = 0 # set when added to DOM

  def setTag(self, tag):
    if tag[0] == LangData.TagNameScopeless:
      self.scopeless = True
      tag = tag[1:]
    self.tag = tag

  def addParameter(self, key, value):
    self.parameters[key] = value

  def appendChild(self, child):
    self.children.append(child)
    child.parent = self
    child.depth = self.depth +1

  def appendText(self, text):
    try: lastNodeTag = self.children[-1].tag
    except IndexError: lastNodeTag = None
    if lastNodeTag == '__text__':
      self.children[-1].text += ' ' + text
    else:
      self.appendChild(DomNodeText(text))

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
