import os
from argparse import ArgumentParser
from Namespace import Namespace
from shp.shp import SHP

def main(args):
  source = os.path.abspath(args.source).replace('\\', '/')
  target = os.path.abspath(args.target).replace('\\', '/')
  shp = SHP(source, target)
  if args.watch:
    shp.watch()
  else:
    shp.compile()

if __name__ == '__main__':
  ap = ArgumentParser()
  ap.add_argument('source', help='Path to the SHP source file')
  ap.add_argument('target', help='Path to the target HTML file')
  ap.add_argument('-w', '--watch',
    help='Use this flag to recompile whenever the source file is edited',
    action='store_true')
  main(ap.parse_args())
