#!/usr/bin/python

import cPickle
import gzip
import subprocess
import tempfile
import re
import sys

line_taken_re = re.compile('^\s*(\d+):\s*(\d+):')

working_dir = tempfile.mkdtemp()

def compile_bin(src):
  global working_dir

  try:
    subprocess.check_output(["gcc", "-o", "%s/bin" % working_dir,
                             "-fprofile-arcs", "-ftest-coverage",
                             src, "-lm"],
                            stderr=subprocess.STDOUT)
  except subprocess.CalledProcessError as e:
    print "Compilation failed"
    print e.output
    return None

  return "%s/bin" % working_dir

def run_test(bin, test):
  try:
    output = subprocess.check_output([bin] + test.split(), shell=True)
    return (output, 0)
  except subprocess.CalledProcessError as e:
    return (e.output, e.returncode)

def get_coverage(src):
  ret = set([])
  gcda = "%s.gcda" % src[:src.rfind('.')]

  subprocess.check_output(["gcov", "-bc", gcda])
  gcov_out = open("%s.gcov" % src)

  for l in gcov_out:
    taken = line_taken_re.match(l)

    if taken:
      times = int(taken.group(1))
      lineno = int(taken.group(2))

      if times > 0:
        ret.add(lineno)

  gcov_out.close()
  os.unlink(gcda)

  return ret

def run_tests(src, bin, tests, golden_outputs):
  ret = []

  try:
    os.unlink("%s.gcda" % src[:src.rfind('.')])
  except:
    pass

  i = 0
  for l in tests:
    sys.stdout.write("%d\r" % i)
    sys.stdout.flush()
    i += 1

    if l not in golden_outputs:
      continue

    expected = golden_outputs[l]
    res = run_test(bin, l)
    correct = (res == expected)

    coverage = get_coverage(src)

    ret.append((correct, coverage))

  print ""
  return ret

if __name__ == '__main__':
  import sys
  import os

  mutated_src = sys.argv[1]
  testvecs = sys.argv[2]
  golden_outputs = sys.argv[3]
  feature_file = sys.argv[4]

  testf = open(testvecs)
  srcbase = os.path.basename(mutated_src)

  goldenf = gzip.GzipFile(golden_outputs, 'rb')
  golden = cPickle.load(goldenf)
  goldenf.close()

  bin = compile_bin(mutated_src)
  features = run_tests(srcbase, bin, testf, golden)

  testf.close()

  outf = gzip.GzipFile(feature_file, 'wb')
  cPickle.dump(features, outf, -1)
  outf.close()

  os.system("rm -rf %s" % working_dir)
