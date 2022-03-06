
class ShpError(Exception):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.__suppress_context__ = True

  def getInfo(self):
    errName = self.__class__.__name__
    errInfo = self.args[0] if len(self.args) else '?'
    return f'{errName}: {errInfo}'

class ShpOriginError(ShpError):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.originSource = None
    self.originNode = None

  def setOrigin(self, source, node):
    self.originSource = source
    self.originNode = node
    return self

  def getInfo(self):
    errName = self.__class__.__name__
    errInfo = self.args[0] if len(self.args) else '?'
    if self.originSource is None or self.originNode is None:
      return f'{errName} (no origin set): {errInfo}'
    file = source.path.split('/')[-1]
    return f'{errName} in {file} at {self.node.pos}: {errInfo}'



# class ShpLexerError(ShpOriginError):
#   pass



# class ShpParserError(ShpOriginError):
#   pass



class ShpCompileError(ShpError):
  pass
class ShpFileNotFoundError(ShpCompileError):
  def __init__(self, path, *args, **kwargs):
    msg = f'File "{path}" does not exist'
    super().__init__(msg, *args, **kwargs)



class ShpFunctionError(ShpOriginError):
  def setCall(self, call):
    self.setOrigin(call.originalSource, call.node)
    return self
class ShpFunctionNotFoundError(ShpFunctionError):
  def __init__(self, funcName, *args, **kwargs):
    msg = f'No function named "{funcName}"'
    super().__init__(msg, *args, **kwargs)
class ShpFunctionParamNotFoundError(ShpFunctionError):
  def __init__(self, funcName, paramName, *args, **kwargs):
    msg = f'Function "{funcName}" requires parameter {paramName}'
    super().__init__(msg, *args, **kwargs)
class ShpFunctionParamInvalidError(ShpFunctionError):
  def __init__(self, funcName, paramName, *args, **kwargs):
    msg = f'Function "{funcName}" has invalid value of parameter {paramName}'
    super().__init__(msg, *args, **kwargs)
class ShpFunctionImplementationError(ShpFunctionError):
  def __init__(self, funcName, *args, **kwargs):
    msg = f'Error in implementation of "{funcName}"'
    super().__init__(msg, *args, **kwargs)
class ShpDefinitionNotFoundError(ShpFunctionError):
  def __init__(self, path, *args, **kwargs):
    msg = f'Definition with path "{path}" does not exist'
    super().__init__(msg, *args, **kwargs)
class ShpDefinitionRepeatedError(ShpFunctionError):
  def __init__(self, path, *args, **kwargs):
    path = '/'.join(path)
    msg = f'Definition with path "{path}" is already defined elsewhere'
    super().__init__(msg, *args, **kwargs)



# class ShpBuildError(ShpError):
#   pass
