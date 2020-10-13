
class Builder:

  def build(self, dom):
    result = ''
    for child in dom.children:
      result += self.buildNode(child)
    return result

  def buildNode(self, node, inlineText=False):
    indent = "  "*node.depth
    if node.isText:
      if inlineText: return node.text
      else: return f'{indent}{node.text}\n'
    try: isSingleTextNode = len(node.children) == 1 and node.children[0].isText
    except IndexError: isSingleTextNode = False
    closeInNewLine = not isSingleTextNode and len(node.children)

    result = f'{indent}<{node.tag}'
    for key, val in node.parameters.items():
      if val.startswith("'"): result += f' {key}={val}'
      else: result += f" {key}='{val}'"
    result += '>'
    if node.scopeless:
      return result + '\n'
    if closeInNewLine: result += '\n'
    for child in node.children:
      result += self.buildNode(child, isSingleTextNode)
    if closeInNewLine: result += indent
    result += f'</{node.tag}>\n'
    return result

  def minify(self, html):
    pairs = [
      ['\n',' '], ['  ',' '],
      ['> ', '>'], ['> ', '>'],
      ['< ','<'], ['< ','<'],
    ]
    for a, b in pairs:
      while a in html:
        html = html.replace(a, b)
    return html
