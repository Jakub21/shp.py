from src.Lexer import Lexer
from src.Parser import Parser
from src.Builder import Builder

from Namespace import Namespace
from time import sleep
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

class Compiler:
  def __init__(self, path, target):
    self.path = path
    self.target = target
    self.lexer = Lexer()
    self.parser = Parser()
    self.builder = Builder()

  def compile(self, minify):
    print(f'Compiling {self.path}')
    with open(self.path, 'r') as file:
      raw = file.read()
    self.lexer.tokenize(raw)
    self.parser.parse(self.lexer.tokens)
    html = self.builder.build(self.parser.dom)
    if minify: html = self.builder.minify(html)
    with open(self.target, 'w', newline='\n') as file:
      file.write(html)

  def watch(self, minify):
    print(f'Watching {self.path}')
    path = self.getSanitizedPath()
    eventHandler = EventHandler(path.fn, self.compile, [minify])
    observer = Observer()
    observer.schedule(eventHandler, path.dir, recursive=False)
    observer.start()
    try:
      while True:
        sleep(.1)
    except KeyboardInterrupt:
      observer.stop()
    observer.join()

  def getSanitizedPath(self):
    pathChunks = self.path.replace('\\','/').split('/')
    return Namespace(dir='/'.join(pathChunks[:-1]), fn=pathChunks[-1])


class EventHandler(PatternMatchingEventHandler):
  def __init__(self, fn, callback, args):
    super().__init__(patterns=['*/'+fn])
    self.callback = callback
    self.args = args
  def on_modified(self, event):
    self.callback(*self.args)
