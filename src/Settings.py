
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
  Literal = '\''
  Comment = '//'

  TokenSeparators = [
    TagOpen, TagClose,
    ScopeOpen, ScopeClose,
    Literal
  ]
