"""
Static HTML Preprocessor
Jakub21, 2023 Q2
--------------------------------
CLI handler class.
"""

from argparse import ArgumentParser


class CLIHandler:
  def __init__(self):
    args = self.parse_args()
    self.sources = args.source
    self.targets = args.target
    print(self.sources)
    print(self.targets)

  @staticmethod
  def parse_args():
    parser = ArgumentParser(
      'shp',
      description='This is a CLI interface for the SHP package. Please refer to the readme for more details.',
    )
    parser.add_argument('-s', '--source', nargs='+', help='Entry point SHP file to be converted.')
    parser.add_argument('-t', '--target', nargs='+', help='Entry point SHP file to be converted.')
    return parser.parse_args()
