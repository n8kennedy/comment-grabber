"""
  comment_grabber.py
  Nate Kennedy
  2013-10-18

  read a collection of files and, based on each file's extension, try to parse
  out any commented text.

  Understood languages, with expected extensions:
    python: .py
    javascript: .js
    c#: .cs
    html: .html
    css: .css
    vbscript: .asp
    common lisp: .lisp
    clojure: .clj
"""

map = {
  '.js': [ '//', '/\*', '\*/' ],
  '.py': [ '#', '^\s*"""', '"""\s*$' ],
  '.cs': [ '//', '/\*', '\*/' ],
  '.php': [ '//', '/\*', '\*/' ],
  '.html': [ None, '<!--', '-->' ],
  '.css' : [ None, '/\*', '*\/' ],
  '.asp' : [ '\'', '<!--', '-->' ],
  '.lisp' : [ ';', '^\s*"', '"\s*$' ],
  '.clj' : [ ';', '^\s*"', '"\s*$' ]
}

def main(*files):
  """iterate over a list of filenames, trying to print commented lines from
  each file.  if a file can't be parsed, print an error and move on"""
  for fil in files:
    print
    print fil
    try:
      ext, lines = get_type_and_lines(fil)
      inline, blockStart, blockEnd = get_patterns(ext)
      for l in iter_grab(lines, inline, blockStart, blockEnd):
        print l
    except Exception as ex:
      print ex.message

def get_type_and_lines(filename):
  """get a file's extension and each line in the file, as a list.
  
  return: (extension, lines)"""
  from os import path

  if path.isfile(filename):
    root, ext = path.splitext(filename)

    hndl = open(filename)
    l = hndl.readlines()
    hndl.close()

    return ext, l
  else:
    raise Exception("{0} is not a file".format(filename))

def get_patterns(ext):
  """check our pattern map for an entry keyed by extension.  if we find a
  match, return a tuple of three regular expressions; otherwise, raise an error

  return: ( inline, blockStart, blockEnd )"""
  def _orNull(ptrn):
    import re
    if ptrn is None:
      return None
    else:
      return re.compile(ptrn)

  if map.has_key(ext):
    l = map[ext]
    return _orNull(l[0]), _orNull(l[1]), _orNull(l[2])
  else:
    raise Exception("Unknown filetype: {0}".format(ext))


def check(re, l):
  """return true if a line contains a match for a regular expression.
  if re is None (or not an re), simply return false"""
  if re is None or not hasattr(re, 'search'):
    return False
  else:
    return not re.search(l) is None

def iter_grab(lines, inline, blockStart, blockEnd):
  """iterate thru lines, checking each against the provided regexes.  if a
  line matches inline, append it to acc.  if a line matches blockStart, begin a
  sub-accumulator, into which all lines up to the next match for blockEnd will
  be added.  when blockEnd is hit, extend our sub-accumulator into our primary,
  and set the sub-acc to None.  Any lines not matching inline or between the
  start and end of a block, will not be returned.

  regexes can be None, but if blockStart is provided, blockEnd must ALSO be
  provided; otherwise an exception is raised """
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

def setuptools_main():
  """entry point function for setup tools"""
  import sys
  files = [f for f in sys.argv[1:] if f[0] != '-']
  main(*files)

if __name__ == '__main__':
  setuptools_main()

