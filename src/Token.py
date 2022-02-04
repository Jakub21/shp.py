from Namespace import Namespace
from src.Settings import LangData

class Position:
  def __init__(self, line, char):
    self.line, self.char = line, char
  def __str__(self):
    return f'[{self.line+1}:{self.char+1}]'

class Token:
  def __init__(self, text, pos, literal=False):
    self.text = text
    self.setPos(pos)
    self.updateType()

  def __str__(self):
    pos = str(self.pos)
    return f'<Token {self.type} \'{self.text}\'{" "*(12-len(self.text))} @{pos}>'

  def append(self, text):
    self.text += text
    self.updateType()

  def isEmpty(self):
    return self.text == ''

  def setPos(self, pos):
    self.pos = pos

  def updateType(self):
    updated = False
    langDataDict = {k:eval(f'LangData.{k}') for k in dir(LangData)
      if not k.startswith('_')}
    for key, val in langDataDict.items():
      if self.text.startswith(val):
        self.type = key
        updated = True
    if not updated:
      self.type = 'Text'
