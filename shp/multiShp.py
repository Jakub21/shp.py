from shp.shp import SHP

class MultiSHP:
  def __init__(self):
    self.shps = []

  def add(self, source, target):
    self.shps += [SHP(source, target)]

  def compile(self):
    for shp in self.shps:
      shp.compile()

  def watch(self, noBlock=False):
    for shp in self.shps:
      shp.onUpdate()
    if not noBlock: self.run()

  def stop(self):
    for shp in self.shps:
      shp.stop()

  def run(self):
    print('[SHP] Press Ctrl+C to stop')
    try:
      while True:
        sleep(.1)
    except KeyboardInterrupt:
      self.stop()
