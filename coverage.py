#!/usr/bin/python

import subprocess
import re
import os
import tempfile
import difflib

branch_re = 'branch *(\d+) taken (\d+)( \(fallthrough\))?'
branches = re.compile(branch_re)

line_taken_re = '^\s*(\d+):\s*(\d+):'
line_taken = re.compile(line_taken_re)

line_not_taken_re = '^\s*\D+:\s*(\d+):'
line_not_taken = re.compile(line_not_taken_re)

linemap = None

def run(testvec):
  os.system("rm *.gcda")
  os.system("./bin %s > /dev/null 2> /dev/null" % testvec)
  
def make_map(fn1, fn2):
  global linemap

  f1 = open(fn1)
  l1 = f1.readlines()
  f1.close()

  f2 = open(fn2)
  l2 = f2.readlines()
  f2.close()

  seq = difflib.SequenceMatcher()
  seq.set_seq1(l1)
  seq.set_seq2(l2)
  blocks = seq.get_matching_blocks()

  linemap = {}
  blockidx = 0
  block = blocks[blockidx]
  blockoffset = 0
  blockstart = block.a
  blocklim = blockstart + block.size

  for i in xrange(len(l1)):
    if i >= blocklim:
      blockoffset = 0
      blockidx += 1
      block = blocks[blockidx]
      blockstart = block.a
      blocklim = blockstart + block.size

    if i < blockstart:
      linemap[i] = block.b - 1
    else:
      linemap[i] = block.b + blockoffset
      blockoffset += 1

def find_lineno(no):
  global linemap

  if linemap is not None:
    return linemap[no]
  else:
    return no

def coverage(src):
  os.system("gcov -bc *.gcda > /dev/null 2> /dev/null")
  raw_data = open("%s.gcov" % os.path.basename(src))
  ret = {}

  for l in raw_data:
    taken = line_taken.match(l)

    if taken:
      times = int(taken.group(1))
      lineno = find_lineno(int(taken.group(2)))

      if times > 0:
        ret[lineno] = True

  raw_data.close()

  #retvec = tuple(ret[lineno] for lineno in sorted(ret))

  ret = tuple(sorted(ret))
  print ret
  return ret

def compile(src):
  os.system("gcc %s -fprofile-arcs -ftest-coverage -O0 -o bin > /dev/null 2> /dev/null" % src)

def all_tests(src, testfile):
  ret = set([])

  compile(src)
  f = open(testfile)

  for l in f:
    run(l.strip())
    ret.add(coverage(src))

  #print len(ret)

if __name__ == '__main__':
  import sys

  src = sys.argv[1]
  testfile = sys.argv[2]

  if len(sys.argv) > 3:
    make_map(sys.argv[1], sys.argv[3])


  vecs = all_tests(src, testfile)

  #for v in vecs:
  #  print v

