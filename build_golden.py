#!/usr/bin/python

import cPickle
import subprocess
import tempfile

working_dir = tempfile.mkdtemp()

def compile_golden(src):
  global working_dir

  try:
    subprocess.check_output(["gcc", "-lm", "-o", "%s/bin" % working_dir,
                             src],
                            stderr=subprocess.STDOUT)
  except subprocess.CalledProcessError as e:
    print "Compilation failed"
    print e.output
    return None

  return "%s/bin" % working_dir

def run_test(bin, test, outputs):
  try:
    output = subprocess.check_output([bin] + test.split())
    outputs[test] = (output, 0)
  except subprocess.CalledProcessError as e:
    outputs[test] = (e.output, e.returncode)

def run_tests(bin, tests, outputs):
  i = 0

  for l in tests:
    run_test(bin, l, outputs)

    i += 1
    print i

if __name__ == '__main__':
  import sys
  import os

  golden_src = sys.argv[1]
  testvecs = sys.argv[2]
  golden_outfile = sys.argv[3]

  outputs = {}
  testf = open(testvecs)

  bin = compile_golden(golden_src)
  run_tests(bin, testf, outputs)

  testf.close()

  outf = open(golden_outfile, 'wb')
  cPickle.dump(outputs, outf)
  outf.close()

  os.system("rm -rf %s" % working_dir)
