"""
Static HTML Preprocessor
Jakub21, 2023 Q2
--------------------------------
__init__
Automated file aggregator.
Imports a specific class from all files in the current directory.
Imported class must have the same name as the file but in title case.
"""

__all__ = ["store"]

from importlib import import_module
from pathlib import Path

from namespace import Namespace


def __find(package):
    for file in Path(__file__).parent.glob("*.py"):
        if file.stem.startswith("__"):
            continue
        module = import_module(f'.{file.stem}', package=package)
        store[file.stem] = getattr(module, file.stem.title())


store = Namespace({})
__find('shp.source.executor.functions')
