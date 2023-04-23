"""
Static HTML Preprocessor
Jakub21, 2023 Q2
--------------------------------
Composition rules for the Composer class
"""

from ..common import HTML, HTML_BUILD


class ComposerRule:
  def __init__(self, composer):
    composer.rules.append(self)
    self.composer = composer

  def __str__(self):
    return f'<Rule {self.__class__.__name__}>'

  def run_open(self):
    raise NotImplementedError
    # return string to append to the result

  def run_close(self):
    raise NotImplementedError
    # return string to append to the result


class RuleTagName(ComposerRule):
  def run_open(self):
    if self.composer.current.type_ != 'Tag':
      return
    return HTML_BUILD.TagNameOpenStart.format(indent = HTML_BUILD.Indent * self.composer.current.depth,
                                              tag = self.composer.current.tag)

  def run_close(self):
    if self.composer.current.type_ != 'Tag':
      return
    if self.composer.current.tag in HTML.Void:
      return
    return HTML_BUILD.TagNameClose.format(indent = HTML_BUILD.Indent * self.composer.current.depth,
                                          tag = self.composer.current.tag)


class RuleAttributes(ComposerRule):
  def run_open(self):
    if self.composer.current.type_ != 'Tag':
      return
    attributes = ''
    for key, values in self.composer.current.attributes.items():
      value = HTML_BUILD.TagAttributeValueSep.join(values)
      attributes += HTML_BUILD.TagAttribute.format(key=key, value=value)
    end = HTML_BUILD.TagNameOpenEndVoid if self.composer.current.tag in HTML.Void else HTML_BUILD.TagNameOpenEndScoped
    return attributes + end

  def run_close(self):
    return


class RuleAppendContent(ComposerRule):
  def run_open(self):
    content = self.composer.current.shortContent()
    if not content:
      return
    indent = HTML_BUILD.Indent * self.composer.current.depth
    return f'\n{indent}{HTML_BUILD.Content.format(content=content)}'

  def run_close(self):
    return
