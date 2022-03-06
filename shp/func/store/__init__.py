
def __find():
  from os import walk, path
  result = []

  directory = path.dirname(path.realpath(__file__)).replace('\\', '/')
  folder = 'shp.func.store'
  _, _, filenames = next(walk(directory))
  for file in filenames:
    if file.startswith('__'): continue
    module = file.split('.')[0]
    result.append(f'from {folder}.{module} import {module}')
  return result

[exec(x) for x in __find()]
