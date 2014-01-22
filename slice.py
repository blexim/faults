#!/usr/bin/python

import sys

f1 = open(sys.argv[1])
f2 = open(sys.argv[2])

passed = open(sys.argv[3], 'w')
failed = open(sys.argv[4], 'w')

linelim = int(sys.argv[5])

def add(l, f):
  t = set(eval(l))

  for i in xrange(linelim):
    if (i+1) in t:
      f.write("1 ")
    else:
      f.write("0 ")

  f.write("\n")

for (l1, l2) in zip(f1, f2):
  if l1 != l2:
    add(l1, failed)
  else:
    add(l1, passed)

f1.close()
f2.close()

passed.close()
failed.close()
