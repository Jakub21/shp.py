"""
Static HTML Preprocessor
Jakub21, 2023 Q2
--------------------------------
Builder class wraps the entire procedure.
"""


from ..compiler import Compiler, Dependency


class Builder:
  def __init__(self, source, target):
    self.source = source
    self.target = target

  def run(self):
    dep = Dependency(self.source)
    comp = Compiler(dep)
    result = comp.compile()
    with open(self.target, 'w') as file:
      file.write(result)
