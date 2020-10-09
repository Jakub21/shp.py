from src.Settings import LangData
from src.DomNode import DomNode
from src.FunctionNode import FunctionNode

class ParserState:
  def __init__(self, parser):
    self.parser = parser

class ParserStateDefault(ParserState):
  def parseToken(self, token):
    if token.isTagOpen():
      self.parser.state = ParserStateTag(self.parser)
    elif token.isTagName():
      node = DomNode(token.text[1:], token.isTagNameScopeless())
      self.parser.currentScope.appendChild(node)
      self.parser.lastTag = node
    elif token.isFunctionName():
      func = FunctionNode(token.text[1:])
      func.setParent(self.parser.currentScope)
      self.parser.funcCalls.append(func)
      self.parser.lastTag = func
    elif token.isScope():
      self.parser.state = ParserStateScope(self.parser)
      self.parser.state.parseToken(token)
    else:
      self.parser.currentScope.appendText(token.text)

class ParserStateTag(ParserState):
  def __init__(self, parser):
    super().__init__(parser)
    self.node = self.parser.lastTag
    self.index = 0
    self.lastParamKey = ''
  def parseToken(self, token):
    if token.isTagClose():
      self.parser.state = ParserStateDefault(self.parser)
    elif token.isTagId():
      self.node.parameters['id'] = token.text[1:]
    elif token.isTagClass():
      try: self.node.parameters['class'] += ' '+token.text[1:]
      except KeyError: self.node.parameters['class'] = token.text[1:]
    elif token.isTagFlagParam():
      self.node.parameters[token.text[1:]] = 'true'
    else:
      self.index += 1
      if self.index % 2: self.lastParamKey = token.text
      else: self.node.addParameter(self.lastParamKey, token.text)

class ParserStateScope(ParserState):
  def parseToken(self, token):
    if token.isScopeOpen():
      self.parser.currentScope = self.parser.lastTag
    elif token.isScopeClose():
      self.parser.currentScope = self.parser.currentScope.parent
    self.parser.state = ParserStateDefault(self.parser)
