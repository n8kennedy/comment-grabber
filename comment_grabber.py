"""
  comment-grabber.py
  Nate Kennedy
  2013-10-18

  get the comment lines from a file

  core function: take file and a structure of regexes (need to accomodate the
  inline comment markers, and the start and end of blocks; could do keyword
  and assume only one inline, one block start, and one block end per language)

  get index of each line in file matching our regexes, one list each for
  inlines, block starts and block ends

  block starts and block ends have to be matched up so that the lines in
  between them are appropriately grabbed

  then just select out all the indexed lines from the file; return as a list
  of lines

  took a recursive approach
"""

map = {
  ".js": [ '//', '/*', '*/' ],
  ".py": [ '#', '"""', '"""' ],
  ".cs": [ '//', '/*', '*/' ],
  ".html": [ None, '<!--', '-->' ]
}

def main(**kwargs):
  def _orNull(key):
    if kwargs.has_key(key):
      return kwargs[key]
    else:
      return None

  # unpack args
  file = _orNull('file')

  type, lines = get_type_and_lines(file)

  inline, blockStart, blockEnd = get_patterns(type)
  print file
  for l in grab(lines, inline, blockStart, blockEnd):
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

def grab(lines, inline, blockStart, blockEnd, acc = None):
  if blockStart is not None and blockEnd is None:
    raise Exception("block marker mismatch")

  if lines is None or len(lines) == 0:
    return []
  elif check( inline, lines[0] ):
    o = [ lines[0].strip() ]
    o.extend( grab( lines[1:], inline, blockStart, blockEnd ) )
    return o
  elif acc is not None and check( blockEnd, lines[0] ):
    acc.append( lines[0].strip() )
    acc.extend( grab( lines[1:], inline, blockStart, blockEnd ) )
    return acc
  elif acc is not None:
    acc.append( lines[0].strip() )
    return grab( lines[1:], inline, blockStart, blockEnd, acc )
  elif check( blockStart, lines[0] ):
    return grab( lines[1:], inline, blockStart, blockEnd, [ lines[0].strip() ] )
  else:
    return grab( lines[1:], inline, blockStart, blockEnd )

if __name__ == '__main__':
  import sys, os
  main(file = os.path.abspath(sys.argv[1]))
