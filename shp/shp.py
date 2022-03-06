from shp.compiler.Compiler import Compiler
from shp.Watchdog import Watchdog
from time import sleep

# Enable colors
import os
os.system("")

def errPrint(shp, error):
  format = '\u001b[91m'
  reset = '\u001b[0m'
  header = f'SHP error while building "{shp.target}"'
  location = f'  In file "{error.originSource.path}" at {error.originNode.pos}\n' if hasattr(error, 'originSource') else ''
  content = f'  {error.__class__.__name__}: {" ".join(error.args)}'
  print(f'{format}{header}\n{location}{content}{reset}')


class SHP:
  def __init__(self, source, target):
    self.compiler = Compiler(source)
    self.source = self.sanitize(source)
    self.target = self.sanitize(target)
    self.watchdog = Watchdog(lambda: self.onUpdate())
    self.watchdog.updateWatchList([self.source])

  def compile(self):
    print(f'[SHP] Compiling "{self.target}"')
    result = self.compiler.compile()
    if result.success:
      with open(self.target, 'w') as file:
        file.write(result.html)
    else:
      errPrint(self, result.error)
    return result.success

  def watch(self, noBlock=False):
    self.onUpdate()
    if not noBlock: self.run()

  def onUpdate(self):
    self.compile()
    paths = [self.source] + [dep.path for dep in self.compiler.dependencies]
    self.watchdog.updateWatchList(paths)

  def stop(self):
    print('[SHP] Interrupted')
    self.watchdog.stopAll()

  def run(self):
    print('[SHP] Press Ctrl+C to stop')
    try:
      while True:
        sleep(.1)
    except KeyboardInterrupt:
      self.stop()

  @staticmethod
  def sanitize(path):
    return path.replace('\\', '/')
