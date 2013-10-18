"""
  comment-grabber.py
  Nate Kennedy
  2013-10-18

  get the comment lines from a file

  based on filetype, use regexes to find following lines 

  core function: take file and a structure of regexes (need to accomodate the
  inline comment markers, and the start and end of blocks; could do keyword
  and assume only one inline, one block start, and one block end per language)

  get index of each line in file matching our regexes, one list each for
  inlines, block starts and block ends

  block starts and block ends have to be matched up so that the lines in
  between them are appropriately grabbed

  then just select out all the indexed lines from the file; return as a list
  of lines

  butt-simple approach:
    one loop over each line in file; at each step, check against each of our
    regexes
"""

def main(**kwargs):
  pass

# def grab_comments(file, 

def grab(lines, inline, blockStart, blockEnd, acc = None):
  if lines is empty:
    return []
  else if inline.match( lines[0] ):
    o = [ lines[0] ]
    o.extend(grab( lines[1:], inline, blockStart, blockEnd) )
    return o
  else if acc is not None and blockEnd.match(lines[0]):
    acc.append( lines[0] )
    acc.extend( grab( lines[1:], inline, blockStart, blockEnd ) )
    return acc
  else if acc is not None
    acc.append( lines[0] )
    return grab( lines[1:], inline, blockStart, blockEnd, acc ) )
  else if blockStart.match( lines[0] )
    return grab( lines[1:], inline, bockStart, blockEnd, [ lines[0] ] ) )
  else
    return grab( lines[1:], inline, blockStart, blockEnd )
