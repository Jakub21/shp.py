import os
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class Watchdog:
  def __init__(self, callback):
    self.watchers = []
    self.callback = callback

  def updateWatchList(self, watchlist):
    self.addToWatchList(watchlist)
    for watcher in self.watchers:
      if watcher.path not in watchlist:
        self.removeWatcher(watcher)

  def addToWatchList(self, watchlist):
    for path in watchlist:
      if self.isWatching(path): continue
      try: self.addWatcher(FileWatcher(path, self.callback))
      except FileNotFoundError:
        print(f'[Watchdog] Can not watch file that does not exist ({path})')

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
    eventHandler = EventHandler(path, callback)
    self.path = path
    self.observer = Observer()
    self.observer.schedule(eventHandler, dir, recursive=False)
    self.observer.start()

  def stop(self):
    self.observer.stop()
    self.observer.join()


class EventHandler(PatternMatchingEventHandler):
  def __init__(self, path, callback, *args):
    super().__init__(patterns=['*/'+path.split('/')[-1]])
    self.path = path
    self.callback = callback
    self.args = args

  def on_modified(self, event):
    print(f'[Watchdog] Detected changes in "{self.path}"')
    self.callback(*self.args)
