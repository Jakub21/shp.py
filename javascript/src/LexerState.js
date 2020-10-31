
class LexerState {
  constructor(lexer) {
    this.lexer = lexer;
    let ld = LangData;
    this.characters = {
      structural: [ld.TagOpen, ld.TagClose, ld.ScopeOpen, ld.ScopeClose],
      whitespace: [' ', '\t', '\r', '\n'],
    };
  }
  apply() {
    this.lexer.tokens.push(this.lexer.currentToken);
    this.lexer.currentToken = new Token('', new Position(0, 0));
  }
  lcheck(line, pos, what) {
    return line.substr(pos.char).startsWith(what);
  }
  lcheckCategory(line, pos, name) {
    let result = false;
    let chars = this.characters[name];
    if (chars == undefined) {
      throw new Error(`Undefined character category ${name}`);
    }
    for (let c of chars) {
      result = this.lcheck(line, pos, c) || result;
      if (result) break;
    }
    return result;
  }
}

class LexerStateNormal extends LexerState {
  tokenize(line, pos) {
    if (this.lexer.currentToken.isEmpty()) {
      this.lexer.currentToken.setPos(pos);
    }
    if (this.lcheck(line, pos, LangData.Comment)) {
      this.lexer.state = new LexerStateComment(this.lexer);
      return;
    }
    if (this.lcheck(line, pos, LangData.Literal)) {
      this.lexer.state = new LexerStateLiteral(this.lexer);
    }
    if (this.lcheckCategory(line, pos, 'structural')) {
      if (!this.lexer.currentToken.isEmpty()) this.apply();
      this.lexer.currentToken.setPos(pos);
      this.lexer.currentToken.append(line[pos.char]);
      this.apply();
    } else if (this.lcheckCategory(line, pos, 'whitespace')) {
      if (!this.lexer.currentToken.isEmpty()) this.apply();
    } else {
      this.lexer.currentToken.append(line[pos.char]);
    }
  }
}

class LexerStateLiteral extends LexerState {
  tokenize(line, pos) {
    this.lexer.currentToken.append(line[pos.char]);
    if (this.lcheck(line, pos, LangData.Literal)) {
      this.apply();
      this.lexer.state = new LexerStateNormal(this.lexer);
    }
  }
}

class LexerStateComment extends LexerState {
  tokenize(line, pos) {
    if (this.lcheck(line, pos, '\n')) {
      this.lexer.state = new LexerStateNormal(this.lexer);
    }
  }
}
