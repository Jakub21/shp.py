"""
Static HTML Preprocessor
Jakub21, 2022 Q4
--------------------------------
Lexer base class. Converts raw text to a list of tokens.
"""

__all__ = ["Lexer"]

from ..common.errors import LexerUnmatchedLiteralError
from ..common.position import Position
from .states import StateDefault, StateLiteral, get_state
from .token import Token


class Lexer:
    def __init__(self, dependency, data=None):
        self.dependency = dependency  # dependency reference for error tracking
        self.state = StateDefault(self)  # current state
        self.data = data  # data fed to the lexer
        self.tokens = []  # list of tokens
        self.position = Position(0, 0)  # pointer to the current position
        self.currentToken = Token()  # currently edited token

    def tokenize(self):
        for char in self.data:
            self.state.tokenize()
            self.position.advance(char)
        self.validate()

    def validate(self):
        # TODO: Make an actual validator
        if isinstance(self.state, StateLiteral):
            raise LexerUnmatchedLiteralError(self.dependency)

    def change_state(self, name):
        self.state = get_state(name)(self, self.state)

    def previous_state(self):
        self.state = self.state.spawnedFrom

    def next_token(self, data=""):
        if not self.currentToken.is_null():
            self.tokens.append(self.currentToken)
        self.currentToken = Token(data, self.position.copy())

    def match(self, what):
        index = self.position.index
        return self.data[index:].startswith(what)

    def match_any(self, what):
        return any([self.match(elm) for elm in what])

    @property
    def current_char(self):
        return self.data[self.position.index]
