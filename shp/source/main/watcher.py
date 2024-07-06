"""
Static HTML Preprocessor
Jakub21, 2023 Q2
--------------------------------
Watcher keeps the output up to date when the source is modified.
"""

from time import sleep
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from .builder import Builder


class Watcher:
  observer: Observer

  def __init__(self, source, target):
    self.source = source
    self.target = target
    self.builder = Builder(source, target)

  def run(self, blocking=True):
    handler = EventHandler(self)
    self.observer = Observer()
    self.observer.schedule(handler, str(self.source.parent))
    self.observer.start()
    if blocking:
      self.block()

  def block(self):
    try:
      while True:
        sleep(0.1)
    except KeyboardInterrupt:
      self.stop()

  def stop(self):
    self.observer.stop()
    self.observer.join()


class EventHandler(PatternMatchingEventHandler):
  def __init__(self, watcher):
    super().__init__(patterns=[str(watcher.source)])
    self.watcher = watcher

  def on_modified(self, event):
    self.watcher.builder.run()
