
class Lexer {
  constructor() {
    this.reset();
  }
  reset(parent) {
    this.tokens = [];
    this.currentToken = new Token('', new Position(0, 0));
    this.state = new LexerStateNormal(this);
  }
  tokenize(text) {
    this.reset();
    let lines = text.split('\n');
    let lineNo = 0;
    for (let line of lines) {
      line += '\n'; // for comment end detection
      for (let charNo = 0; charNo < line.length; charNo += 1) {
        this.state.tokenize(line, new Position(lineNo, charNo));
      }
      lineNo += 1;
    }
  }
}
