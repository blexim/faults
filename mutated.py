#!/usr/bin/python

import cPickle
import gzip
import subprocess
import tempfile
import re
import sys
import difflib

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
    output = subprocess.check_output("%s %s" % (bin, test), shell=True)
    return (output, 0)
  except subprocess.CalledProcessError as e:
    return (e.output, e.returncode)

def get_coverage(src):
  ret = set([])
  gcda = "%s.gcda" % src[:src.rfind('.')]

  try:
    subprocess.check_output(["gcov", "-bc", gcda])
    gcov_out = open("%s.gcov" % src)
  except:
    return set([])

  for l in gcov_out:
    taken = line_taken_re.match(l)

    if taken:
      times = int(taken.group(1))
      lineno = int(taken.group(2))

      if times > 0:
        ret.add(lineno)

  gcov_out.close()

  return ret

def run_tests(src, bin, tests, golden_outputs):
  ret = []

  i = 0
  for l in tests:
    sys.stdout.write("%d\r" % i)
    sys.stdout.flush()
    i += 1

    if l not in golden_outputs:
      continue

    expected = golden_outputs[l]

    try:
      os.unlink("%s.gcda" % src[:src.rfind('.')])
    except:
      pass

    res = run_test(bin, l)
    correct = (res == expected)

    if res[1] >= 0:
      coverage = get_coverage(src)
    else:
      # terminated by a signal -- probably segfault...
      coverage = set([])

    ret.append((correct, coverage))

  print ""
  return ret

def find_bugs(orig, mutated):
  f1 = open(orig)
  l1 = f1.readlines()
  f1.close()

  f2 = open(mutated)
  l2 = f2.readlines()
  f2.close()

  seq = difflib.SequenceMatcher()
  seq.set_seq1(l1)
  seq.set_seq2(l2)

  blocks = seq.get_matching_blocks()

  ret = []

  lastmatch = 0

  for (c1, c2, n) in blocks:
    if n != 0:
      ret += range(lastmatch+1, c2+1)
      lastmatch = c2 + n

  return ret


if __name__ == '__main__':
  import sys
  import os

  if len(sys.argv) < 6:
    print "Usage: ./mutated.py <golden.c> <mutated.c> <testvectors> <golden outputs> <features>"
    sys.exit()


  golden_src = sys.argv[1]
  mutated_src = sys.argv[2]
  testvecs = sys.argv[3]
  golden_outputs = sys.argv[4]
  feature_file = sys.argv[5]

  bugs = find_bugs(golden_src, mutated_src)
  print "Bugs: %s" % str(bugs)

  testf = open(testvecs)
  srcbase = os.path.basename(mutated_src)

  goldenf = gzip.GzipFile(golden_outputs, 'rb')
  golden = cPickle.load(goldenf)
  goldenf.close()

  bin = compile_bin(mutated_src)
  features = run_tests(srcbase, bin, testf, golden)

  testf.close()

  outf = gzip.GzipFile(feature_file, 'wb')
  cPickle.dump((bugs, features), outf, -1)
  outf.close()

  os.system("rm -rf %s" % working_dir)
