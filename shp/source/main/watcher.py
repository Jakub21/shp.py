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

from ..common.errors import ShpError
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
    def __init__(self, source, target):
        super().__init__(target=self.run)
        self.source = source
        self.target = target
        self.builder = Builder(source, target)
        self.stopped = False
        self.needs_refresh = False
        self.dependencies = []
        self.observers = []

    def run(self):
        try:
            self.builder.run()
        except ShpError as e:
            self.print_shp_err(e)
        self.dependencies = self.builder.dependencies
        self.start_observer()
        self.block()

    def start_observer(self):
        self.observers = []
        for path in [self.source, *[dep.path for dep in self.dependencies]]:
            handler = EventHandler(self, path)
            observer = Observer()
            observer.schedule(handler, str(path.parent), recursive=True)
            observer.start()
            self.observers += [observer]

    def block(self):
        try:
            while not self.stopped:
                if self.needs_refresh:
                    self.refresh()
                sleep(0.1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self):
        for observer in self.observers:
            observer.stop()
            observer.join()
        self.stopped = True

    def refresh(self):
        self.needs_refresh = False
        for observer in self.observers:
            observer.stop()
            observer.join()
        self.start_observer()

    def build(self):
        try:
            self.builder.run()
        except ShpError as e:
            self.print_shp_err(e)
        if self.dependencies != self.builder.dependencies:
            self.needs_refresh = True

    def print_shp_err(self, error):
        print(f"SHP: {error.__class__.__name__}: {error}", end="\n\n")


class EventHandler(PatternMatchingEventHandler):
    def __init__(self, runner, path):
        self.runner = runner
        patterns = [str(path)]
        super().__init__(patterns=patterns)

    def on_modified(self, event):
        self.runner.build()
