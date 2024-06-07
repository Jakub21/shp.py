"""
Static HTML Preprocessor
Jakub21, 2023 Q2
--------------------------------
Implementation of a lang function.
"""

from ..base.lang_function import LangFunction
from ...common import HTML, HTML_BUILD, FunctionMissingParameterError, DefinitionDuplicateError
from ...parser import Node


class Slot(LangFunction):

  def at_traverse(self):
    pass

  def at_extend(self):
    pass

  def at_define(self):
    try:
      slot_id = self.node.attributes.id[-1]
    except LookupError:
      raise FunctionMissingParameterError(self.dependency, self.node.position, self.node.tag, 'id') from None
    if slot_id in self.executor.doc_data.slots.keys():
      raise DefinitionDuplicateError(self.dependency, self.node.position, 'slot', slot_id)
    self.executor.doc_data.slots[slot_id] = self.node

  def at_finalize(self):
    pass
