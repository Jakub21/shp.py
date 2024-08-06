"""
Static HTML Preprocessor
Jakub21, 2023 Q2
--------------------------------
Builder class wraps the entire procedure.
"""


from ..compiler import Compiler, Dependency


class Builder:
  dependencies: [Dependency]

  def __init__(self, source, target):
    self.source = source
    self.target = target
    self.dependency = Dependency(self.source)
    self.dependencies = []

  def run(self):
    print('SHP: Building')
    compiler = Compiler(self.dependency)
    self.dependencies = compiler.dependencies
    result = compiler.compile()
    with open(self.target, 'w') as file:
      file.write(result)
