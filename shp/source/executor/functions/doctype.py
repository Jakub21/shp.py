"""
Static HTML Preprocessor
Jakub21, 2023 Q2
--------------------------------
Implementation of a lang function.
"""

from ..base.lang_function import LangFunction
from ...common import HTML, HTML_BUILD
from ...parser import Node


class Doctype(LangFunction):

  def at_traverse(self):
    pass

  def at_extend(self):
    pass

  def at_define(self):
    pass

  def at_finalize(self):
    try:
      doctype = self.node.attributes['id'][-1]
    except LookupError:
      doctype = HTML.DoctypeDefault
    clause = HTML_BUILD.DoctypeClause.format(doctype = doctype)
    doctype = Node.Content(self.node.position, clause)
    self.node.replace_with(doctype)
