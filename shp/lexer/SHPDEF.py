from Namespace import Namespace

SHPDEF = Namespace(
  TagOpen = '[',
  TagClose = ']',
  TagNameScoped = '$',
  TagNameScopeless = '%',
  TagId = '#',
  TagClass = '.',
  TagFlagParam = '!',
  ScopeOpen = '{',
  ScopeClose = '}',
  FunctionName = '@',
  Literal = '\'',
  Comment = '//',
  DefaultDoctype = 'HTML',
  IncludePathFromRoot = '*/',
  IncludePathBack = '^',
)
