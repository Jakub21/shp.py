from shp.lexer.Position import Position
from shp.lexer.SHPDEF import SHPDEF

class Token:
  def __init__(self, data='', pos=None):
    self.data = data
    self.followingSpace = ''
    self.pos = Position(0,0) if pos is None else pos
    self.detectType()

  def __str__(self):
    return f'<Token {self.type} "{self.data}" {self.pos}>'

  def initalize(self, pos):
    if self.isEmpty():
      self.pos = pos

  def append(self, data):
    self.data += data
    self.detectType()

  def appendSpace(self, data):
    self.followingSpace += data

  def isEmpty(self):
    return self.data == ''

  def detectType(self):
    updated = False
    for key, prefix in SHPDEF.items():
      if self.data.startswith(prefix):
        self.type = key
        updated = True
    if not updated:
      self.type = 'Text'
