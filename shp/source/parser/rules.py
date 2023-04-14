"""
Static HTML Preprocessor
Jakub21, 2022 Q4
--------------------------------
Individual parsing rules used by parser states.
"""

from .node import Node


class ParserRule:
  def __init__(self, parserState, isDefault=False):
    self.parser = parserState.parser
    if not isDefault:
      parserState.rules.append(self)

  def __str__(self):
    return f'<Rule {self.__class__.__name__}>'

  def run(self):
    raise NotImplementedError
    # return True to continue processing the current token
    # return False to stop


class RuleEnterNodeAttrs(ParserRule):
  def run(self):
    if not self.parser.currentToken.matchTypes(['AttrOpen']):
      return True
    self.parser.changeState('StateTagAttrs')
    self.parser.select(self.parser.selection.children[-1])
    return False


class RuleNewNode(ParserRule):
  def run(self):
    if self.parser.currentToken.matchTypes(['Tag', 'TagPre', 'TagFunc']):
      node = Node.FromToken(self.parser.currentToken)
      self.parser.selection.appendNode(node)
      return False
    return True


class RuleEnterScope(ParserRule):
  def run(self):
    if not self.parser.currentToken.matchTypes(['ScopeOpen']):
      return True
    self.parser.select(self.parser.selection.children[-1])


class RuleExitScope(ParserRule):
  def run(self):
    if not self.parser.currentToken.matchTypes(['ScopeClose']):
      return True
    self.parser.select(self.parser.selection.parent)
    return False


class RuleAppendContent(ParserRule):
  def run(self):
    if not self.parser.currentToken.matchTypes(['Text']):
      return True
    if self.appendToLastNode():
      return False
    node = Node.FromToken(self.parser.currentToken)
    self.parser.selection.appendNode(node)
    return False

  def appendToLastNode(self):
    try:
      lastNode = self.parser.selection.children[-1]
    except IndexError:
      return False
    if lastNode.type_ != 'Content':
      return False
    lastNode.content += self.parser.currentToken.fullData
    return True


class RuleAttrsQuickID(ParserRule):
  def run(self):
    if not self.parser.currentToken.matchTypes(['QuickID']):
      return True
    self.parser.selection.addAttribute('id', self.parser.currentToken.noprefix)
    return False


class RuleAttrsQuickClass(ParserRule):
  def run(self):
    if not self.parser.currentToken.matchTypes(['QuickClass']):
      return True
    self.parser.selection.addAttribute('class', self.parser.currentToken.noprefix)
    return False


class RuleAttrsQuickFlag(ParserRule):
  def run(self):
    if self.parser.currentToken.matchTypes(['QuickFlagTrue']):
      self.parser.selection.addAttribute(self.parser.currentToken.noprefix, 'true')
      return False
    if self.parser.currentToken.matchTypes(['QuickFlagFalse']):
      self.parser.selection.addAttribute(self.parser.currentToken.noprefix, 'false')
      return False
    return True


class RuleAttrsKeyValCycle(ParserRule):
  def run(self):
    
    return False  # must be the last rule, can process all tokens


class RuleExitNodeAttrs(ParserRule):
  def run(self):
    if not self.parser.currentToken.matchTypes(['AttrClose']):
      return True
    self.parser.changeState('StateDefault')
    self.parser.select(self.parser.selection.parent)
    return False


# class RuleExitPreformatted(ParserRule):
#   def run(self):
#     return True