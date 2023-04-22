"""
Static HTML Preprocessor
Jakub21, 2023 Q2
--------------------------------
__init__
This is adapted from a very old aggregate.
The only viable alternative was manually maintained list, so it had to be used.
There were available some advanced loaders but all of them break relative imports.
"""

__all__ = ['store']

from pathlib import Path
from namespace import Namespace


def __find():
  for file in Path(__file__).parent.glob('*.py'):
    if file.stem.startswith('__'):
      continue
    exec(f'from .{file.stem} import {file.stem.title()}')
    store[file.stem] = eval(file.stem.title(), globals(), locals())


store = Namespace({})
__find()
