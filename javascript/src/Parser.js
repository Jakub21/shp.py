
class Parser {
  constructor(root) {
    this.reset(root);
  }

  reset(root) {
    this.state = new ParserStateDefault(this);
    this.root = root;
    this.currentScope = this.root;
    this.lastNode = this.root;
  }

  parse(tokens) {
    this.reset(this.root);
    for (let token of tokens) {
      this.state.parseToken(token);
    }
  }
}
