"""
Static HTML Preprocessor
Jakub21, 2023 Q2
--------------------------------
Watcher keeps the output up to date when the source is modified.
"""

from threading import Thread
from time import sleep
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from .builder import Builder


class Watcher:
  def __init__(self, pairs):
    self.pairs = pairs
    self.runners = []

  def run(self, blocking=True):
    for source, target in self.pairs:
      runner = Runner(source, target)
      self.runners += [runner]
      runner.start()
    if blocking:
      self.block()

  def block(self):
    try:
      while True:
        sleep(0.1)
    except KeyboardInterrupt:
      self.stop()

  def stop(self):
    for runner in self.runners:
      runner.stop()
      runner.join()


class Runner(Thread):
  observer: Observer

  def __init__(self, source, target):
    super().__init__(target=self.run)
    self.source = source
    self.target = target
    self.builder = Builder(source, target)
    self.stopped = False
    self.needs_refresh = False
    self.dependencies = []

  def run(self):
    self.builder.run()
    self.dependencies = self.builder.dependencies
    self.start_observer()
    self.block()

  def start_observer(self):
    handler = EventHandler(self)
    self.observer = Observer()
    self.observer.schedule(handler, str(self.source.parent), recursive=True)
    self.observer.start()

  def block(self):
    try:
      while not self.stopped:
        if self.needs_refresh:
          self.refresh()
        sleep(0.1)
    except KeyboardInterrupt:
      self.stop()

  def stop(self):
    self.observer.stop()
    self.observer.join()
    self.stopped = True

  def refresh(self):
    self.needs_refresh = False
    self.observer.stop()
    self.observer.join()
    self.start_observer()

  def build(self):
    self.builder.run()

    if self.dependencies != self.builder.dependencies:
      self.needs_refresh = True


class EventHandler(PatternMatchingEventHandler):
  def __init__(self, runner):
    patterns = [str(runner.source), *[str(dep.path) for dep in runner.dependencies]]
    print('patterns', patterns)
    super().__init__(patterns=patterns)
    self.runner = runner

  def on_modified(self, event):
    self.runner.build()
