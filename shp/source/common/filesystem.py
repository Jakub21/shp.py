"""
Static HTML Preprocessor
Jakub21, 2023 Q2
--------------------------------
Universal file path solver.
"""

from pathlib import Path

from ..common.LANG import LANG


def resolve_path(dependency, raw_path):
  raw_path = raw_path.strip('"')
  path = dependency.path.parent
  while raw_path.startswith(LANG.PATH.ParentDir):
    raw_path = raw_path[len(LANG.PATH.ParentDir):]
    path = path.parent
  return Path(path, *raw_path.split(LANG.PATH.Separator)).with_suffix('.shp')
