"""
Static HTML Preprocessor
Jakub21, 2022 Q4
--------------------------------
All special characters in the SHP markup and HTML data for the auto void tag
detection feature
"""

__all__ = ['LANG', 'HTML']

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
    Variable = '?',
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
  Literal = '"',
  Escape = '\\',
  Comment = '//',
)

HTML = Namespace(
  Doctype = 'HTML',
  Scopeless = ['area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input',
    'link', 'meta', 'param', 'source', 'track', 'wbr'
  ],
  Preformatted = ['pre'],
)

# Scopeless https://developer.mozilla.org/en-US/docs/Glossary/Void_element
