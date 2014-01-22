#!/usr/bin/python

import sys

f1 = open(sys.argv[1])
f2 = open(sys.argv[2])

for (l1, l2) in zip(f1, f2):
  if l1 != l2:
    print l1.strip()

f1.close()
f2.close()
