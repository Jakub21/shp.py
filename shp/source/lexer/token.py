"""
Static HTML Preprocessor
Jakub21, 2022 Q4
--------------------------------
Token
"""

from ..common.LANG import TOKEN_TYPE


class Token:
  def __init__(self, data='', position=None):
    self.type_ = None
    self.data = data
    self._tail = ''
    self.position = position.copy() if position is not None else None
    self.escaped = False
    self.detectType()

  def __str__(self):
    return f'<Token "{self.data}" {self.position} | {self.type_}>'

  def append(self, data):
    self.data += data
    self.detectType()

  def appendTail(self, space=' '):
    self._tail += space

  def setEscaped(self):
    self.escaped = True

  def isNull(self):
    return (not self.data) or (self.position is None)

  def reInit(self, position):
    if not self.isNull():
      return
    self.position = position.copy()
    self.data = ''
    self._tail = ''
    self.detectType()

  def detectType(self):
    if self.isNull():
      self.type_ = 'Null'
      return
    match = {key: self.data.startswith(val) for key, val in TOKEN_TYPE.items()}
    if True not in match.values() or self.escaped:
      self.type_ = 'Text'  # TODO
      return
    self.type_ = [key for key in match.keys() if match[key]][0]

  @property
  def noprefix(self):
    try:
      prefix = TOKEN_TYPE[self.type_]
    except KeyError:
      prefix = ''
    return self.data[len(prefix):]

  @property
  def fullData(self):
    return self.data + self._tail

  def matchTypes(self, types):
    return self.type_ in types
