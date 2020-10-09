
class LangData:
  TagOpen = '['
  TagClose = ']'
  TagNameScoped = '$'
  TagNameScopeless = '%'
  TagId = '#'
  TagClass = '.'
  TagFlagParam = '!'
  ScopeOpen = '{'
  ScopeClose = '}'
  FunctionName = '@'
  Literal = '\''
  Comment = '//'

  TokenSeparators = [
    TagOpen, TagClose,
    ScopeOpen, ScopeClose,
    Literal
  ]


class LangFunctions:
  @staticmethod
  def define(func, parser, scope):
    parser.definitions[func.parameters.id] = func.children

  @staticmethod
  def paste(func, parser, scope):
    try: children = parser.definitions[func.parameters.id]
    except KeyError as e:
      raise KeyError(f'"{func.parameters.id}" was not defined, can not paste') from None
    for oldChild in children[::-1]:
      child = oldChild.duplicate()
      scope.insertChild(child, func.isNthChild)
      scope.recalcSubtreeDepths()
