from os import walk

def build(name, version, repo, license, dir):
  minify = False
  header = f'''// {name} v{version}
// Github {repo}
// {license} License
'''
  forceNewline = ['class', 'function', 'var', 'let', 'static']
  source = ''
  for path, dirs, files in walk(dir):
    for file in files:
      source += open(f'{dir}/{file}', 'r', encoding='utf-8').read()

  if minify:
    source = source.replace('\n\n', '\n')
    clean = ''
    for line in source.split('\n'):
      for word in forceNewline:
        if line.startswith(word) and not clean.endswith('\n'): clean += '\n'
      if '//' in line: line = line.split('//')[0]
      clean += line
    source = header + clean + '\n'
    while '  ' in source: source = source.replace('  ', ' ')
  return source

if __name__ == '__main__':
  name = 'shp.js'
  version = '0.1'
  repo = 'https://github.com/Jakub21/Static-Html-Preprocessor'
  license = 'MIT'
  dir = './src'
  source = build(name, version, repo, license, dir)
  open(name, 'w', newline='\n').write(source)
