from src.Token import Token
from src.Settings import LangData

class Lexer:

  def tokenize(self, text):
    lines = text.split('\n')
    tokens = []
    for lineNo, line in enumerate(lines):
      if LangData.Comment in line:
        line = line[:line.index(LangData.Comment)]
      for c in LangData.TokenSeparators:
        line = line.replace(c, f' {c} ')
      for word in line.split():
        tokens.append(Token(word, lineNo+1))
    return self.joinLiteralTokens(tokens)

  def joinLiteralTokens(self, rawTokens):
    inLiteral = False
    literal = None
    tokens = []
    for token in rawTokens:
      if token.isLiteral():
        inLiteral = not inLiteral
        if inLiteral: literal = Token('', token.line, True)
        else:
          literal.text = literal.text[1:]
          tokens.append(literal)
      elif inLiteral:
        literal.text += ' ' + token.text
      elif not inLiteral:
        tokens.append(token)
    return tokens
