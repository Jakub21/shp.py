from os import path as op
from shp.lexer.SHPDEF import SHPDEF
from shp.func.Function import Function
from shp.parser.Nodes import NodeData

class FuncDoctype(Function):
  name = 'doctype'

  def execute(self):
    try: id = self.params.id
    except AttributeError:
      id = SHPDEF.DefaultDoctype
    newNode = NodeData(f'<!DOCTYPE {id}>', self.node.pos)
    self.node.replaceSelf(newNode)
