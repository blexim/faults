#!/usr/bin/python

import cPickle
import gzip
import subprocess
import tempfile
import sys

working_dir = tempfile.mkdtemp()

def compile_bin(src):
  global working_dir

  try:
    subprocess.check_output(["gcc", "-o", "%s/bin" % working_dir,
                             src, "-lm"],
                            stderr=subprocess.STDOUT)
  except subprocess.CalledProcessError as e:
    print "Compilation failed"
    print e.output
    return None

  return "%s/bin" % working_dir

def run_test(bin, test, outputs):
  try:
    output = subprocess.check_output([bin] + test.split(), shell=True)
    outputs[test] = (output, 0)
  except subprocess.CalledProcessError as e:
    outputs[test] = (e.output, e.returncode)

def run_tests(bin, tests, outputs):
  i = 0

  for l in tests:
    sys.stdout.write("%d\r" % i)
    sys.stdout.flush()

    run_test(bin, l, outputs)

    i += 1

  print ""

if __name__ == '__main__':
  import sys
  import os

  if len(sys.argv) < 4:
    print "Usage: ./golden.py <golden.c> <test vectors> <golden outputs>"
    sys.exit()

  golden_src = sys.argv[1]
  testvecs = sys.argv[2]
  golden_outfile = sys.argv[3]

  outputs = {}
  testf = open(testvecs)

  bin = compile_bin(golden_src)
  run_tests(bin, testf, outputs)

  testf.close()

  outf = gzip.GzipFile(golden_outfile, 'wb')
  cPickle.dump(outputs, outf, -1)
  outf.close()

  os.system("rm -rf %s" % working_dir)
