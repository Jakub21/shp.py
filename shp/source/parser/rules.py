"""
Static HTML Preprocessor
Jakub21, 2022 Q4
--------------------------------
Individual parsing rules used by parser states.
"""

from ..common.errors import ParserAttributeOrderError
from ..common.lang_data import TOKEN_TYPE
from .node import Node


class ParserRule:
    def __init__(self, parser_state, is_default=False):
        self.parser = parser_state.parser
        if not is_default:
            parser_state.rules.append(self)

    def __str__(self):
        return f"<Rule {self.__class__.__name__}>"

    def run(self):
        raise NotImplementedError
        # return True to continue processing the current token
        # return False to stop


class RuleEnterNodeAttrs(ParserRule):
    def run(self):
        if not self.parser.current_token.match_types(["AttrOpen"]):
            return True
        self.parser.change_state("StateTagAttrs")
        self.parser.select(self.parser.selection.children[-1])
        return False


class RuleNewNode(ParserRule):
    def run(self):
        if self.parser.current_token.match_types(["Tag", "TagPre", "TagFunc"]):
            node = Node.FromToken(self.parser.current_token)
            self.parser.selection.append_node(node)
            return False
        return True


class RuleEnterScope(ParserRule):
    def run(self):
        if not self.parser.current_token.match_types(["ScopeOpen"]):
            return True
        self.parser.select(self.parser.selection.children[-1])


class RuleExitScope(ParserRule):
    def run(self):
        if not self.parser.current_token.match_types(["ScopeClose"]):
            return True
        self.parser.select(self.parser.selection.parent)
        return False


class RuleAppendContent(ParserRule):
    def run(self):
        if not self.parser.current_token.match_types(["Text"]):
            return True
        if self.append_to_last_node():
            return False
        node = Node.FromToken(self.parser.current_token)
        self.parser.selection.append_node(node)
        return False

    def append_to_last_node(self):
        try:
            last_node = self.parser.selection.children[-1]
        except IndexError:
            return False
        if last_node.type_ != "Content":
            return False
        last_node.content += self.parser.current_token.full_data
        return True


class RuleAttrsQuickID(ParserRule):
    def run(self):
        if not self.parser.current_token.match_types(["QuickID"]):
            return True
        self.parser.selection.add_attribute("id", self.parser.current_token.suffix)
        return False


class RuleAttrsQuickClass(ParserRule):
    def run(self):
        if not self.parser.current_token.match_types(["QuickClass"]):
            return True
        self.parser.selection.add_attribute("class", self.parser.current_token.suffix)
        return False


class RuleAttrsQuickFlag(ParserRule):
    def run(self):
        if self.parser.current_token.match_types(["QuickFlagTrue"]):
            self.parser.selection.add_attribute(
                self.parser.current_token.suffix, "true"
            )
            return False
        if self.parser.current_token.match_types(["QuickFlagFalse"]):
            self.parser.selection.add_attribute(
                self.parser.current_token.suffix, "false"
            )
            return False
        return True


class RuleAttrsKeyValCycle(ParserRule):
    def run(self):
        if self.parser.state.phase == self.parser.state.Phases.KEY:
            self.check_is_val_sign(False)
            self.parser.state.current_key = self.parser.current_token.data
        if self.parser.state.phase == self.parser.state.Phases.EQUALS:
            self.check_is_val_sign(True)
        if self.parser.state.phase == self.parser.state.Phases.VALUE:
            self.check_is_val_sign(False)
            self.parser.selection.add_attribute(
                self.parser.state.current_key, self.parser.current_token.data
            )
        self.parser.state.next_phase()
        return False  # must be the last rule, can process all tokens

    def check_is_val_sign(self, expected):
        match = self.parser.current_token.data == TOKEN_TYPE.AttrValue
        if match and not expected:
            raise ParserAttributeOrderError(
                self.parser.dependency,
                self.parser.current_token.position,
                f"Unexpected {TOKEN_TYPE.AttrValue} sign",
            )
        if not match and expected:
            raise ParserAttributeOrderError(
                self.parser.dependency,
                self.parser.current_token.position,
                f"Expected {TOKEN_TYPE.AttrValue} sign",
            )


class RuleExitNodeAttrs(ParserRule):
    def run(self):
        if not self.parser.current_token.match_types(["AttrClose"]):
            return True
        self.parser.change_state("StateDefault")
        self.parser.select(self.parser.selection.parent)
        return False
