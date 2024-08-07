"""
Static HTML Preprocessor
Jakub21, 2022 Q4
--------------------------------
Token
"""

from ..common.lang_data import TOKEN_TYPE


class Token:
    def __init__(self, data="", position=None):
        self.type_ = None
        self.data = data
        self._tail = ""
        self.position = position.copy() if position is not None else None
        self.escaped = False
        self.detect_type()

    def __str__(self):
        return f'<Token "{self.data}" {self.position} | {self.type_}>'

    def append(self, data):
        self.data += data
        self.detect_type()

    def append_tail(self, space=" "):
        self._tail += space

    def set_escaped(self):
        self.escaped = True

    def is_null(self):
        return (not self.data) or (self.position is None)

    def re_init(self, position):
        if not self.is_null():
            return
        self.position = position.copy()
        self.data = ""
        self._tail = ""
        self.detect_type()

    def detect_type(self):
        if self.is_null():
            self.type_ = "Null"
            return
        match = {key: self.data.startswith(val) for key, val in TOKEN_TYPE.items()}
        if True not in match.values() or self.escaped:
            self.type_ = "Text"  # TODO
            return
        self.type_ = next(key for key in match.keys() if match[key])

    @property
    def suffix(self):
        try:
            prefix = TOKEN_TYPE[self.type_]
        except KeyError:
            prefix = ""
        return self.data[len(prefix) :]

    @property
    def full_data(self):
        return self.data + self._tail

    def match_types(self, types):
        return self.type_ in types
