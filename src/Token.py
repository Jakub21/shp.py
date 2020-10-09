from src.Settings import LangData

class Token:
  def __init__(self, text, line, literal=False):
    self.text = text
    self.line = line
    self.literal = literal

  def __str__(self):
    return f'<Token \'{self.text}\' @{self.line}>'

  def isLiteral(self):
    return self.text == LangData.Literal

  def isTagOpen(self):
    return self.text == LangData.TagOpen
  def isTagClose(self):
    return self.text == LangData.TagClose

  def isTagName(self):
    return self.isTagNameScoped() or self.isTagNameScopeless()
  def isTagNameScoped(self):
    return self.text.startswith(LangData.TagNameScoped)
  def isTagNameScopeless(self):
    return self.text.startswith(LangData.TagNameScopeless)

  def isTagId(self):
    return self.text.startswith(LangData.TagId)
  def isTagClass(self):
    return self.text.startswith(LangData.TagClass)
  def isTagFlagParam(self):
    return self.text.startswith(LangData.TagFlagParam)

  def isScope(self):
    return self.isScopeOpen() or self.isScopeClose()
  def isScopeOpen(self):
    return self.text == LangData.ScopeOpen
  def isScopeClose(self):
    return self.text == LangData.ScopeClose

  def isFunctionName(self):
    return self.text.startswith(LangData.FunctionName)
  def isFunctionContent(self):
    return self.text == LangData.FunctionContent
  def isFunctionClose(self):
    return self.text == LangData.FunctionClose
