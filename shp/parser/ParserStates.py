from shp.parser.Nodes import Node, NodeScoped, NodeFunction
from Namespace import Namespace

class ParserState:
  def __init__(self, parser):
    self.parser = parser
    self.tagPrefixes = ['TagNameScoped', 'TagNameScopeless', 'FunctionName']
    self.paramPrefixes = ['TagId', 'TagClass', 'TagFlagParam']

  def switchState(self, other):
    self.parser.state = other(self.parser)

  def checkType(self, token, compare, depth=0):
    if type(compare) == str:
      return token.type == compare
    else:
      return True in [self.checkType(token, entry, depth+1)
        for entry in compare]


class ParserStateDefault(ParserState):
  def parse(self, token):
    if self.checkTagOpen(token): return
    if self.checkTagName(token): return
    if self.checkScopeChange(token): return
    self.parser.currentScope.appendData(token.data, token.pos)

  def checkTagOpen(self, token):
    if self.checkType(token, 'TagOpen'):
      self.switchState(ParserStateTag)
      return True

  def checkTagName(self, token):
    if self.checkType(token, self.tagPrefixes):
      node = Namespace(
        TagNameScopeless = Node,
        TagNameScoped = NodeScoped,
        FunctionName = NodeFunction
      )[token.type](token.data[1:], token.pos)
      self.parser.currentScope.appendNode(node)
      self.parser.lastAddedTag = node
      return True

  def checkScopeChange(self, token):
    if self.checkType(token, ['ScopeOpen', 'ScopeClose']):
      self.switchState(ParserStateScope)
      self.parser.state.parse(token)
      return True


class ParserStateTag(ParserState):
  def __init__(self, parser):
    super().__init__(parser)
    self.index = 0;
    self.lastKey = '';

  def parse(self, token):
    if self.checkType(token, 'TagClose'):
      self.switchState(ParserStateDefault)
      return
    if self.checkType(token, self.paramPrefixes):
      self.parsePrefixedParam(token)
      return
    self.parseIndexedParam(token)

  def parsePrefixedParam(self, token):
    node = self.parser.lastAddedTag
    value = token.data[1:]
    Namespace(
      TagId = lambda n: n.addParam('id', value),
      TagClass = lambda n: n.addParam('class', value),
      TagFlagParam = lambda n: n.addParam(value, True),
    )[token.type](node)

  def parseIndexedParam(self, token):
    self.index += 1
    if self.index % 2:
      self.lastKey = token.data
    else:
      self.parser.lastAddedTag.addParam(self.lastKey, token.data)


class ParserStateScope(ParserState):
  def parse(self, token):
    if self.checkType(token, 'ScopeOpen'):
      self.parser.currentScope = self.parser.lastAddedTag
    elif self.checkType(token, 'ScopeClose'):
      self.parser.currentScope = self.parser.currentScope.parent
    self.switchState(ParserStateDefault)
