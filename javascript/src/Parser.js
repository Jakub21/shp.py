
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
