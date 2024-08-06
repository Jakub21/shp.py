"""
Static HTML Preprocessor
Jakub21, 2023 Q2
--------------------------------
CLI handler class.
"""

from argparse import ArgumentParser
from pathlib import Path
from os import getcwd

from .builder import Builder
from .watcher import Watcher


class CLIHandler:
  def __init__(self):
    args = self.parse_args()
    cwd = Path(getcwd())
    action_method = self.watch if args.watch else self.build
    action_method(Path(cwd, args.source).resolve(), Path(cwd, args.target).resolve())

  def build(self, source, target):
    builder = Builder(source, target)
    builder.run()

  def watch(self, source, target):
    watcher = Watcher([(source, target)])
    watcher.run(blocking=True)

  @staticmethod
  def parse_args():
    parser = ArgumentParser(
      'shp',
      description='This is a CLI interface for the SHP package. Please refer to the readme for more details.',
    )
    parser.add_argument('source', help='SHP file to be converted.')
    parser.add_argument('target', help='Result file path.')
    parser.add_argument('-w', '--watch', action='store_true', help='Enable input file watchdog.')
    return parser.parse_args()
