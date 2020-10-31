
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
