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

def run_test(bin, test, outputs, golden_outputs):
  args = [s for s in test.split() if s != '<']

  try:
    output = subprocess.check_output([bin] + test.split(), shell=False)
    res = (output, 0)
  except subprocess.CalledProcessError as e:
    res = (e.output, e.returncode)

  if golden_outputs is None:
    outputs[test] = res
  else:
    if test in golden_outputs:
      golden_res = golden_outputs[test]
      outputs[test] = (res == golden_res)

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
  outfile = sys.argv[3]

  if len(sys.argv) > 4:
    golden = gzip.GzipFile(sys.argv[4], 'rb')
    (golden_outputs, _, _) = cPickle.load(golden)
    golden.close()
  else:
    golden_outputs = None

  outputs = {}
  testf = open(testvecs)

  bin = compile_bin(golden_src)
  run_tests(bin, testf, outputs)

  testf.close()

  outf = gzip.GzipFile(golden_outfile, 'wb')
  cPickle.dump(outputs, outf, -1)
  outf.close()

  os.system("rm -rf %s" % working_dir)
