#!/usr/bin/python

import cPickle
import gzip
import subprocess
import tempfile

working_dir = tempfile.mkdtemp()

def compile_bin(src):
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

def get_coverage(src):
  gcda = "%s.gcda" % src[:src.rfind('.')]
  f = open(gcda, "rb")
  ret = f.read()
  f.close()
  os.unlink(gcda)

  return ret

def get_gcno(src):
  src = os.path.basename(src)
  gcno = "%s.gcno" % src[:src.rfind('.')]
  f = open(gcno, "rb")
  ret = f.read()
  f.close()

  return ret

def run_tests(src, bin, tests, outputs, golden_outputs, coverage):
  i = 0

  try:
    os.unlink("%s.gcda" % src[:src.rfind('.')])
  except:
    pass

  for l in tests:
    print i
    run_test(bin, l.strip(), outputs, golden_outputs)
    coverage[l] = get_coverage(src)

    i += 1

if __name__ == '__main__':
  import sys
  import os

  if len(sys.argv) < 3:
    print "Usage: %s <src> <test vectors> <output file> [golden outputs]" % sys.argv[0]
    sys.exit()

  src = sys.argv[1]
  testvecs = sys.argv[2]
  outfile = sys.argv[3]

  if len(sys.argv) > 4:
    golden = gzip.GzipFile(sys.argv[4], 'rb')
    (golden_outputs, _, _) = cPickle.load(golden)
    golden.close()
  else:
    golden_outputs = None

  outputs = {}
  coverage = {}
  testf = open(testvecs)
  srcbase = os.path.basename(src)

  bin = compile_bin(src)
  run_tests(srcbase, bin, testf, outputs, golden_outputs, coverage)
  gcno = get_gcno(src)

  testf.close()

  outf = gzip.GzipFile(outfile, 'wb')
  cPickle.dump((outputs, gcno, coverage), outf, True)
  outf.close()

  os.system("rm -rf %s" % working_dir)
