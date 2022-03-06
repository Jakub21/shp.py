from shp.errors import *
from Namespace import Namespace

class Store:
  def __init__(self):
    self.store = Namespace()
    self.fill()

  def fill(self):
    import shp.func.store as _store
    for key in dir(_store):
      if key.startswith('__'): continue
      func = eval(f'_store.{key}.{key}')
      self.store[func.name] = func

  def get(self, name):
    try: return self.store[name]
    except:
      raise ShpFunctionNotFoundError(name)

  def getPreDepNames(self):
    return [func.name for func in self.store.values() if func.enablePreDep]


FunctionStore = Store()
