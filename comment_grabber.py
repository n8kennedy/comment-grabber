"""
  comment-grabber.py
  Nate Kennedy
  2013-10-18

  read a collection of files and, based on each file's extension, try to parse
  out any commented text.  Understands python, javascript, c-sharp, and html
"""

map = {
  '.js': [ '\/\/', '\/\*', '\*\/' ],
  '.py': [ '#', '"""', '"""' ],
  '.cs': [ '\/\/', '\/\*', '\*\/' ],
  '.html': [ None, '<!--', '-->' ],
  '.css' : [ None, '\/\*', '\*\/' ],
  '.asp' : [ '\'', None, None ]
}

def main(**kwargs):
  import sys
  def _orNull(key):
    if kwargs.has_key(key):
      return kwargs[key]
    else:
      return None

  # unpack args
  files = _orNull('files')

  for fil in files:
    type, lines = get_type_and_lines(fil)
    inline, blockStart, blockEnd = get_patterns(type)
    print
    print fil
    for l in iter_grab(lines, inline, blockStart, blockEnd):
      print l

def get_type_and_lines(filename):
  from os import path
  root, type = path.splitext(filename)
  hndl = open(filename)
  l = hndl.readlines()
  hndl.close()

  return type, l

def get_patterns(type):
  def _orNull(ptrn):
    import re
    if ptrn is None:
      return None
    else:
      return re.compile(ptrn)
  l = map[type]
  return _orNull(l[0]), _orNull(l[1]), _orNull(l[2])

def check(re, l):
  if re is None or not hasattr(re, 'search'):
    return False
  else:
    return not re.search(l) is None

def iter_grab(lines, inline, blockStart, blockEnd):
  if blockStart is not None and blockEnd is None:
    raise Exception("block marker mismatch")

  acc = []
  block = None

  for l in lines:
    if check(inline, l):
      acc.append(l.strip())
    elif block is not None and check(blockEnd, l):
      block.append(l.strip())
      acc.extend(block)
      block = None
    elif block is not None:
      block.append(l.strip())
    elif check(blockStart, l):
      if check(blockEnd, l):
        acc.append(l.strip())
      else:
        block = [l.strip()]

  return acc

if __name__ == '__main__':
  import sys, os
  files = [f for f in sys.argv[1:] if f[0] != '-']
  main(files = files)
