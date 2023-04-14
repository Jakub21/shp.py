"""
Static HTML Preprocessor
Jakub21, 2022 Q4
--------------------------------
All special characters in the SHP markup and HTML data for the auto void tag
detection feature
"""

__all__ = ['LANG', 'HTML', 'TOKEN_TYPE', 'WHITESPACE']

from Namespace import Namespace

LANG = Namespace(
  TAG = Namespace(
    Normal = '$',
    Preform = '%',
    Function = '@',
    SpaceSuffix = '_',
  ),
  ATTR = Namespace(
    Open = '[',
    Close = ']',
    Value = '=',
  ),
  QUICKATTR = Namespace(
    ID = '#',
    Class = '.',
    FlagTrue = '+',
    FlagFalse = '!',
  ),
  SCOPE = Namespace(
    Open = '{',
    Close = '}',
  ),
  PATH = Namespace(
    ParentDir = '^',
    FromEntry = '_/',
  ),
  Variable = '?',
  Literal = '"',
  Escape = '\\',
  Comment = '//',
)

HTML = Namespace(
  Doctype = 'HTML',
  Void = ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
    'link', 'meta', 'param', 'source', 'track', 'wbr'
  ],
  Preform = ['pre'],
)

TOKEN_TYPE = Namespace(
  # Type = Prefix
  Tag = LANG.TAG.Normal,
  TagPre = LANG.TAG.Preform,
  TagFunc = LANG.TAG.Function,
  AttrOpen = LANG.ATTR.Open,
  AttrClose = LANG.ATTR.Close,
  AttrValue = LANG.ATTR.Value,
  QuickID = LANG.QUICKATTR.ID,
  QuickClass = LANG.QUICKATTR.Class,
  QuickFlagTrue = LANG.QUICKATTR.FlagTrue,
  QuickFlagFalse = LANG.QUICKATTR.FlagFalse,
  ScopeOpen = LANG.SCOPE.Open,
  ScopeClose = LANG.SCOPE.Close,
  Literal = LANG.Literal,
  Variable = LANG.Variable,
)


WHITESPACE = [' ', '\r', '\n', '\t']

# TODO
# Token with any escaped character is always set to Text type, this could be problematic in the future
