
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
