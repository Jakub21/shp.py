from src.compiler.Compiler import Compiler

c = Compiler('./data/index.shp')
html = c.compile()
with open('./result.html', 'w') as file:
  file.write(html)
