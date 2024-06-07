"""
Static HTML Preprocessor
Jakub21, 2022 Q4
--------------------------------
Various SHP related exceptions
"""


class ShpError(Exception):
  def suffix(self, dependency=None, position=None):
    result = '\n '
    if position is not None:
      result += f' at {position}'
    if dependency is not None:
      result += f' in {dependency.path}'
    return result


########################################


class LexerError(ShpError):
  pass


class LexerUnmatchedLiteralError(LexerError):
  def __init__(self, dependency):
    super().__init__(f'Unexpected end of data: A literal string was not closed {self.suffix(dependency)}')


########################################


class ParserError(ShpError):
  pass


class ParserAttributeOrderError(ParserError):
  def __init__(self, dependency, position, message):
    super().__init__(f'{message} {self.suffix(dependency, position)}')

########################################


class FunctionError(ShpError):
  pass


class DefinitionLookupError(FunctionError):
  def __init__(self, dependency, position, lookup_type, key):
    super().__init__(f'Cannot find {lookup_type} named {key} {self.suffix(dependency, position)}')


class DefinitionDuplicateError(FunctionError):
  def __init__(self, dependency, position, lookup_type, key):
    super().__init__(f'{lookup_type} named {key} already exists {self.suffix(dependency, position)}')


class UnknownFunctionError(FunctionError):
  def __init__(self, dependency, position, name):
    super().__init__(f'{name} is not a SHP function {self.suffix(dependency, position)}')


class FunctionMissingParameterError(FunctionError):
  def __init__(self, dependency, position, function_name, parameter_name):
    super().__init__(f'Function {function_name} is missing a required parameter {parameter_name}'
                     f'{self.suffix(dependency, position)}')


########################################


class DependencyNotFoundError(ShpError):
  def __init__(self, dependency):
    super().__init__(f'File {dependency.path} does not exist')
