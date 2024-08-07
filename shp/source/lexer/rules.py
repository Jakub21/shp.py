"""
Static HTML Preprocessor
Jakub21, 2022 Q4
--------------------------------
Individual tokenization rules used by lexer states.
"""

from ..common.lang_data import LANG, TOKEN_TYPE, WHITESPACE


class LexerRule:
    def __init__(self, lexer_state, is_default=False):
        self.lexer = lexer_state.lexer
        if not is_default:
            lexer_state.rules.append(self)

    def __str__(self):
        return f"<Rule {self.__class__.__name__}>"

    def run(self):
        raise NotImplementedError
        # return True to continue processing the current position
        # return False to stop


class RuleAppendChar(LexerRule):
    def run(self):
        self.lexer.current_token.append(self.lexer.current_char)
        return True
        # Fallback rule that always adds current char to the token


class RuleIgnore(LexerRule):
    def run(self):
        return True
        # Fallback rule that always ignores the character


class RulePrevious(LexerRule):
    def run(self):
        self.lexer.previous_state()
        return True


# NOTE: Almost the same as below, could be simplified somehow
class RuleNewlineTail(LexerRule):
    def run(self):
        if self.lexer.match_any("\n"):
            token = self.lexer.current_token
            if token.is_null():
                token = self.lexer.tokens[-1]
            token.append_tail(self.lexer.current_char)
        return True


class RuleWhitespaceTail(LexerRule):
    def run(self):
        if self.lexer.match_any(WHITESPACE):
            if not self.lexer.tokens:
                return False
            token = self.lexer.current_token
            if token.is_null():
                token = self.lexer.tokens[-1]
            token.append_tail(self.lexer.current_char)
        return True


class RuleNextAtWhitespace(LexerRule):
    def run(self):
        if self.lexer.match_any(WHITESPACE):
            if not self.lexer.current_token.is_null():
                self.lexer.next_token()
            return False
        return True


class RuleCommentChar(LexerRule):
    def run(self):
        if self.lexer.match(LANG.Comment):
            self.lexer.change_state("StateComment")
            return False
        return True


class RuleEndCommentAtNewline(LexerRule):
    def run(self):
        if self.lexer.match("\n"):
            self.lexer.previous_state()
        return False


class RuleEscapeChar(LexerRule):
    def run(self):
        if self.lexer.match(LANG.Escape):
            self.lexer.change_state("StateEscape")
            return False
        return True


class RuleMarkEscaped(LexerRule):
    def run(self):
        self.lexer.current_token.set_escaped()
        return True


class RuleLiteralEnter(LexerRule):
    def run(self):
        if self.lexer.match(LANG.Literal):
            self.lexer.current_token.append(self.lexer.current_char)
            self.lexer.change_state("StateLiteral")
            return False
        return True


class RuleLiteralPrevious(LexerRule):
    def run(self):
        if self.lexer.match(LANG.Literal):
            self.lexer.previous_state()
            return True
        return True


class RuleNonPrefixFunctionalChar(LexerRule):
    def run(self):
        chars = [
            LANG.ATTR.Open,
            LANG.ATTR.Close,
            LANG.ATTR.Value,
            LANG.SCOPE.Open,
            LANG.SCOPE.Close,
        ]
        if self.lexer.match_any(chars):
            self.lexer.next_token(self.lexer.current_char)
            self.lexer.next_token()
            return False
        return True


class RuleFunctionalChar(LexerRule):
    def run(self):
        if self.lexer.match_any(TOKEN_TYPE.values()):
            self.lexer.next_token()
        return True
