from argparse import ArgumentParser
from src.Preprocessor import Preprocessor

def main(args):
  pp = Preprocessor(args.path, args.target)
  if args.watch:
    pp.watch(args.minify)
  else:
    pp.compile(args.minify)

if __name__ == '__main__':
  ap = ArgumentParser()
  ap.add_argument('path', help='Path to file you want to compile')
  ap.add_argument('target', help='Path to compiled HTML file')
  ap.add_argument('-w', '--watch', help='Use this flag to recompile whenever file is edited',
    action='store_true')
  ap.add_argument('-m', '--minify', help='Minify the output HTML file',
    action='store_true')
  main(ap.parse_args())
