import os
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class Watchdog:
  def __init__(self, callback):
    self.watchers = []
    self.callback = callback

  def updateWatchList(self, watchlist):
    for path in watchlist:
      if not self.isWatching(path):
        self.addWatcher(FileWatcher(path, self.callback))
    for watcher in self.watchers:
      if watcher.path not in watchlist:
        self.removeWatcher(watcher)

  def addWatcher(self, watcher):
    print('[Watchdog] Watching file', watcher.path)
    self.watchers.append(watcher)

  def removeWatcher(self, watcher):
    print('[Watchdog] No longer watching file', watcher.path)
    watcher.stop()
    del self.watchers[self.watchers.index(watcher)]

  def isWatching(self, path):
    return path in map(lambda w: w.path, self.watchers)

  def stopAll(self):
    for watcher in self.watchers:
      watcher.stop()


class FileWatcher:
  def __init__(self, path, callback):
    dir = os.path.dirname(path)
    fn = path.split('/')[-1]
    eventHandler = EventHandler(fn, callback)
    self.path = path
    self.observer = Observer()
    self.observer.schedule(eventHandler, dir, recursive=False)
    self.observer.start()

  def stop(self):
    self.observer.stop()
    self.observer.join()


class EventHandler(PatternMatchingEventHandler):
  def __init__(self, fn, callback, *args):
    super().__init__(patterns=['*/'+fn])
    self.callback = callback
    self.args = args

  def on_modified(self, event):
    self.callback(*self.args)
