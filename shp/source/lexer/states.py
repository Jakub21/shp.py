"""
Static HTML Preprocessor
Jakub21, 2022 Q4
--------------------------------
Lexer states
"""

__all__ = ["get_state", "StateDefault", "StateLiteral"]

from .rules import *
from .token import Token


def get_state(name):
    return eval(name)  # TODO


class LexerState:
    def __init__(self, lexer, current=None):
        self.lexer = lexer
        self.rules = []
        self._default = RuleAppendChar(self, True)
        self.spawnedFrom = current

    def __str__(self):
        return f"<LexerState {self.__class__.__name__}>"

    def ensure_valid_token(self):
        if self.lexer.current_token.is_null():
            self.lexer.current_token = Token("", self.lexer.position)

    def tokenize(self):
        self.ensure_valid_token()
        for rule in self.rules:
            if not rule.run():
                return
        self._default.run()


class StateDefault(LexerState):
    def __init__(self, lexer, current=None):
        super().__init__(lexer, current)
        RuleWhitespaceTail(self)
        RuleNextAtWhitespace(self)
        RuleEscapeChar(self)
        RuleCommentChar(self)
        RuleNonPrefixFunctionalChar(self)
        RuleLiteralEnter(self)
        RuleFunctionalChar(self)


class StateComment(LexerState):
    def __init__(self, lexer, current=None):
        super().__init__(lexer, current)
        RuleEndCommentAtNewline(self)
        self._default = RuleIgnore(self)


class StateLiteral(LexerState):
    def __init__(self, lexer, current=None):
        super().__init__(lexer, current)
        RuleWhitespaceTail(self)
        RuleEscapeChar(self)
        RuleLiteralPrevious(self)


class StateEscape(LexerState):
    def __init__(self, lexer, current=None):
        super().__init__(lexer, current)
        RuleWhitespaceTail(self)
        RulePrevious(self)
        RuleMarkEscaped(self)
