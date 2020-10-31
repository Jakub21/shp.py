
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
