
class Position:
  def __init__(self, line, char):
    self.line, self.char = line, char
  def __str__(self):
    return f'[{self.line+1}:{self.char+1}]'
