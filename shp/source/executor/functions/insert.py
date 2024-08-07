"""
Static HTML Preprocessor
Jakub21, 2023 Q2
--------------------------------
Implementation of a lang function.
"""

from ...common.errors import DefinitionLookupError, FunctionMissingParameterError
from ..base.lang_function import LangFunction


class Insert(LangFunction):
    def at_traverse(self):
        pass

    def at_extend(self):
        pass

    def at_define(self):
        self.node.detach()

    def at_finalize(self):
        try:
            slot_id = self.node.attributes.id[-1]
        except LookupError:
            raise FunctionMissingParameterError(
                self.dependency, self.node.position, self.node.tag, "id"
            ) from None
        try:
            slot = self.executor.doc_data.slots[slot_id]
        except LookupError:
            raise DefinitionLookupError(
                self.dependency, self.node.position, "slot", slot_id
            ) from None
        slot.replace_with(*self.node.children)
