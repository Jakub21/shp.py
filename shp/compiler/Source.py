from os import path as op
from Namespace import Namespace
from shp.errors import *
from shp.lexer.Lexer import Lexer
from shp.parser.Parser import Parser
from shp.func.FunctionStore import FunctionStore

class Source:
  def __init__(self, compiler, path):
    self.compiler = compiler
    self.path = self._sanitizePath(op.abspath(path))
    self.reset()

  def reset(self):
    self.calls = []
    self.dependencies = []
    self.injected = False
    self.parentSource = Namespace(path='None')

  def __str__(self):
    return f'<Source "{self.path}">'

  def addDependency(self, dep):
    dep.parentSource = self
    self.dependencies += [dep]
    self.compiler.addDependency(dep)

  def buildTree(self):
    try: file = open(self.path, 'r')
    except FileNotFoundError:
      raise ShpFileNotFoundError(self.path)
    tokens = Lexer().tokenize(file.read())
    self.treeRoot = Parser().parse(tokens)
    self.findFuncCalls()

  def findFuncCalls(self):
    constraint = lambda n: n.isType('Function')
    funcNodes = self._findNodes(self.treeRoot, constraint)
    for node in funcNodes:
      try: self.calls += [FunctionStore.get(node.tagName)(self, node)]
      except ShpFunctionNotFoundError as err:
        raise err.setOrigin(self, node)

  def injectFuncNode(self, node):
    call = FunctionStore.get(node.tagName)(self, node)
    self.calls += [call]
    self.calls = self._sortFuncCalls(self.calls)
    self.injected = True

  def execPreDep(self):
    for call in self.calls:
      if call.enablePreDep:
        self.safeExecution(call, True)

  def finalize(self):
    calls = self._sortFuncCalls(self.calls)
    for call in self.calls:
      if not call.done:
        self.safeExecution(call)
        self.treeRoot.updateDepth(0)
      if self.injected:
        self.injected = False
        self.finalize()
        break

  def safeExecution(self, call, pre=False):
    try: call.runPreDep() if pre else call.run()
    except ShpFunctionError as err:
      raise err.setCall(call)
    except:
      import traceback
      print('\nOriginal Error', traceback.format_exc())
      raise ShpFunctionImplementationError(call.name).setCall(call)

  def _findNodes(self, node, constraint):
    result = []
    if constraint(node):
      result += [node]
    if node.isType('Scoped'):
      for child in node.children:
        result += self._findNodes(child, constraint)
    return result

  def _sortFuncCalls(self, calls):
    calls = calls[:]
    result = []
    while len(calls):
      legal = [call for call in calls if call.name not in
        [entry for c in calls for entry in c.forceBefore]]
      for call in legal:
        result += [call]
        del calls[calls.index(call)]
    return result

  @staticmethod
  def _sanitizePath(path):
    return path.replace('\\', '/')
