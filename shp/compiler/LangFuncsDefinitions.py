from Namespace import Namespace
from shp.compiler.Definition import Definition
from shp.compiler.ShpDefinitions import ShpDefinitions as SHPDEF
from shp.parser.Nodes import NodeData

def _define(manager, call):
  manager.defs.append(Definition(call))
  call.node.removeSelf()

def _paste(manager, call):
  id = call.node.params.id
  ns = call.ns[:]
  try: ns += [call.node.params['from']]
  except KeyError: pass
  ns = '/'.join(ns)
  matching = list(filter(lambda d: d.id == id and d.ns == ns, manager.defs))
  if len(matching) > 1:
    raise ValueError(str(call)+' More than 1 definition is found')
  if len(matching) == 0:
    raise ValueError(str(call)+' No definitions were found')
  definition = matching[0]
  call.node.replaceSelfList(definition.children)

def _namespace(manager, call):
  if len(call.node.children):
    call.node.replaceSelfList(call.node.children)
  else:
    call.node.removeSelf()

def _doctype(manager, call):
  try: value = call.node.params.id
  except AttributeError: value = SHPDEF.DefaultDoctype
  node = NodeData(f'<!DOCTYPE {value}>', call.node.pos)
  call.node.replaceSelf(node)


definitions = Namespace(
  define = _define,
  paste = _paste,
  namespace = _namespace,
  doctype = _doctype,
)
