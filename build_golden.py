#!/usr/bin/python

import cPickle
import subprocess
import tempfile

working_dir = tempfile.mkdtemp()

def compile_golden(src):
  global working_dir

  try:
    subprocess.check_output(["gcc", "-lm", "-o", "%s/bin" % working_dir,
                             "-fprofile-arcs", "-ftest-coverage",
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

def get_coverage(src):
  gcda = "%s.gcda" % src[:src.rfind('.')]

  subprocess.check_output(["gcov", "-bc", gcda])
  gcov_out = open("%s.gcov" % src)
  ret = gcov_out.read()
  gcov_out.close()

  os.unlink(gcda)

  return ret

def run_tests(src, bin, tests, outputs, coverage):
  i = 0

  os.unlink("%s.gcda" % src[:src.rfind('.')])

  for l in tests:
    run_test(bin, l, outputs)
    coverage[l] = get_coverage(src)

    i += 1
    print i

if __name__ == '__main__':
  import sys
  import os

  golden_src = sys.argv[1]
  testvecs = sys.argv[2]
  golden_outfile = sys.argv[3]

  outputs = {}
  coverage = {}
  testf = open(testvecs)
  srcbase = os.path.basename(golden_src)

  bin = compile_golden(golden_src)
  run_tests(srcbase, bin, testf, outputs, coverage)

  testf.close()

  outf = open(golden_outfile, 'wb')
  cPickle.dump((outputs, coverage), outf)
  outf.close()

  os.system("rm -rf %s" % working_dir)
