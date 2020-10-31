
class ShpCompiler {
  constructor(root) {
    this.lexer = new Lexer();
    this.parser = new Parser(root);
  }
  compile(shp) {
    this.lexer.tokenize(shp);
    this.parser.parse(this.lexer.tokens);
    return this.parser.root;
  }
}
