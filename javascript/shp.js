
class Builder {
  build(node) {
    let result = '';
    for (let child of node.children) {
      result += this.buildNode(child);
    }
    return result;
  }
  buildNode(node) {
    if (node.isText) {
      return node.text;
    }
    let result = `<${node.tag}`;
    for (let [key, val] of Object.entries(node.parameters)) {
      if (val.startsWith("'")) result += ` ${key}=${val}`;
      else result += ` ${key}='${val}'`;
    }
    result += '>';
    if (node.scopeless) {
      return `${result}\n`
    }
    for (let child of node.children) {
      result += this.buildNode(child)
    }
    result += `</${node.tag}>\n`
    return result;
  }
}

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

class Parser {
  constructor() {
    this.reset();
  }

  reset(root) {
    this.state = new ParserStateDefault(this);
    this.root = new ShpNode();
    this.currentScope = this.root;
    this.lastNode = this.root;
  }

  parse(tokens) {
    this.reset();
    for (let token of tokens) {
      this.state.parseToken(token);
    }
  }
}

class ParserState {
  constructor(parser) {
    this.parser = parser;
  }
}

class ParserStateDefault extends ParserState {
  parseToken(token) {
    if (token.type == 'TagOpen') {
      this.parser.state = new ParserStateTag(this.parser);
    } else if (['TagNameScoped', 'TagNameScopeless'].includes(token.type)) {
      let node = new ShpNode(token.text.substr(1));
      this.parser.currentScope.appendChild(node);
      this.parser.lastNode = node;
    } else if (['ScopeOpen', 'ScopeClose'].includes(token.type)) {
      this.parser.state = new ParserStateScope(this.parser);
      this.parser.state.parseToken(token);
    } else {
      this.parser.currentScope.appendChild(new ShpNodeText(token.text + ' '));
    }
  }
}

class ParserStateTag extends ParserState {
  constructor(parser) {
    super(parser);
    this.node = this.parser.lastNode;
    this.index = 0;
    this.lastParamKey = '';
  }
  parseToken(token) {
    if (token.type == 'TagClose') {
      this.parser.state = new ParserStateDefault(this.parser);
    } else if (token.type == 'TagId') {
      this.node.addParameter('id', token.text.substr(1));
    } else if (token.type == 'TagClass') {
      this.node.addParameter('class', token.text.substr(1));
    } else if (token.type == 'TagFlagParam') {
      this.node.addParameter(token.text.substr(1), true);
    } else {
      this.index += 1;
      if (this.index % 2) this.lastParamKey = token.text;
      else this.node.addParameter(this.lastParamKey, token.text);
    }
  }
}

class ParserStateScope extends ParserState {
  parseToken(token) {
    if (token.type == 'ScopeOpen') {
      this.parser.currentScope = this.parser.lastNode;
    } else if (token.type == 'ScopeClose') {
      this.parser.currentScope = this.parser.currentScope.parent;
    }
    this.parser.state = new ParserStateDefault(this.parser);
  }
}

const LangData = {
  TagOpen: '[',
  TagClose: ']',
  TagNameScoped: '$',
  TagNameScopeless: '%',
  TagId: '#',
  TagClass: '.',
  TagFlagParam: '!',
  ScopeOpen: '{',
  ScopeClose: '}',
  FunctionName: '@',
  Literal: '\'',
  Comment: '//',
};

class ShpCompiler {
  constructor(root) {
    this.lexer = new Lexer();
    this.parser = new Parser(root);
    this.builder = new Builder();
  }
  compile(shp) {
    this.lexer.tokenize(shp);
    this.parser.parse(this.lexer.tokens);
    let temp = $create('div');
    temp.innerHTML = this.builder.build(this.parser.root);
    return Array.from(temp.children);
  }
}

class ShpNode {
  constructor(tag, scopeless=false) {
    this.tag = tag;
    this.parameters = {};
    this.children = [];
    this.scopeless = scopeless;
    this.isText = false;
    this.parent = undefined;
  }
  addParameter(key, value) {
    if (this.parameters[key] == undefined) {
      this.parameters[key] = value;
    } else {
      this.parameters[key] += ' ' + value;
    }
  }
  appendChild(child) {
    this.children.push(child);
    child.parent = this;
  }
  appendText(text) {
    let lastNode = this.children[this.children.length-1];
    if (lastNode.tag == '__text__') {
      lastNode.text += ' ' + text;
    } else {
      this.appendChild(new ShpNodeText(text));
    }
  }
}

class ShpNodeText extends ShpNode {
  constructor(text) {
    super('__text__', true);
    this.text = text;
    this.isText = true;
  }
}

class Position {
  constructor(l, c) {
    this.line = l;
    this.char = c;
  }
}

class Token {
  constructor(text, pos, literal=false) {
    this.text = text;
    this.setPos(pos);
    this.updateType();
  }
  append(text) {
    this.text += text;
    this.updateType();
  }
  isEmpty() {
    return !this.text.length;
  }
  setPos(pos) {
    this.pos = pos;
  }
  updateType() {
    let updated = false;
    for (let [key, val] of Object.entries(LangData)) {
      if (this.text.startsWith(val)) {
        this.type = key;
        updated = true;
      }
    }
    if (!updated) {
      this.type = 'Text';
    }
  }
}
