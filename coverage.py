#!/usr/bin/python

import subprocess
import re
import os
import tempfile

branch_re = 'branch *(\d+) taken (\d+)( \(fallthrough\))?'
branches = re.compile(branch_re)

line_taken_re = '^\s*(\d+):\s*(\d+):'
line_taken = re.compile(line_taken_re)

line_not_taken_re = '^\s*\D+:\s*(\d+):'
line_not_taken = re.compile(line_not_taken_re)

tempdir = None
expectedlen = None
golden = None

def run(testvec):
  os.system("./bin %s > /dev/null 2> /dev/null" % testvec)

def coverage(src):
  global expectedlen 
  global golden

  os.system("gcov -bc *.gcda > /dev/null 2> /dev/null")
  raw_data = open("%s.gcov" % os.path.basename(src))
  ret = {}

  for l in raw_data:
    taken = line_taken.match(l)
    not_taken = line_not_taken.match(l)

    if taken:
      times = int(taken.group(1))
      lineno = int(taken.group(2))

      if times > 0:
        ret[lineno] = True
      else:
        ret[lineno] = False
    elif not_taken:
      lineno = int(not_taken.group(1))

      if lineno not in ret:
        ret[lineno] = False

  raw_data.close()

  retvec = tuple(ret[lineno] for lineno in sorted(ret))

  if expectedlen is None:
    golden = ret
    expectedlen = len(retvec)
    os.system("cp %s.gcov golden.gcov" % os.path.basename(src))

  elif len(ret) != expectedlen:
    print "Expected %d saw %d" % (expectedlen, len(retvec))

    os.system("cp %s.gcov bug.gcov" % os.path.basename(src))

    for lineno in ret:
      if lineno not in golden:
        print "New line: %d" % lineno

  return retvec

def compile(src):
  os.system("gcc %s -fprofile-arcs -ftest-coverage -O0 -o bin > /dev/null 2> /dev/null" % src)

def all_tests(src, testfile):
  ret = []
  tempdir = tempfile.mkdtemp()

  compile(src)
  f = open(testfile)

  for l in f:
    run(l.strip())
    ret.append(coverage(src))

  os.system("rm -rf %s" % tempdir)

  return ret

if __name__ == '__main__':
  import sys

  src = sys.argv[1]
  testfile = sys.argv[2]

  vecs = all_tests(src, testfile)

  for v in vecs:
    print v
