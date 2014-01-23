#!/usr/bin/python

import re
import cPickle

line_taken_re = '^\s*(\d+):\s*(\d+):'
line_taken = re.compile(line_taken_re)

def coverage(gcov_data):
  ret = set([])

  for l in gcov_data.split('\n'):
    taken = line_taken.match(l)

    if taken:
      times = int(taken.group(1))
      lineno = int(taken.group(2))

      if times > 0:
        ret.add(lineno)

  return ret

def analyse_test(golden_out, mutated_out, mutated_cov, passed, failed):
  features = coverage(mutated_cov)

  if golden_out == mutated_out:
    passed.append(features)
  else:
    failed.append(features)

def analyse_tests(golden, mutated):
  passed = []
  failed = []

  goldenf = open(golden)
  (golden_outputs, golden_coverage) = cPickle.load(goldenf)
  goldenf.close()

  mutatedf = open(mutated)
  (mutated_outputs, mutated_cov) = cPickle.load(mutatedf)
  mutatedf.close()

  for test in mutated_outputs:
    analyse_test(golden_outputs[test], mutated_outputs[test],
                 mutated_cov[test], passed, failed)

  return (passed, failed)

def dump_matrix(lines, vectors, f):
  for l in lines:
    f.write("%d " % l)

  f.write("\n")

  for features in vectors:
    for l in lines:
      if l in features:
        f.write("1 ")
      else:
        f.write("0 ")
    f.write("\n")

if __name__ == '__main__':
  import sys

  golden = sys.argv[1]
  mutated = sys.argv[2]
  passedfile = sys.argv[3]
  failedfile = sys.argv[4]

  (passed, failed) = analyse_tests(golden, mutated)

  lines = set([])
  for v in passed:
    lines.update(v)
  for v in failed:
    lines.update(v)

  lines = sorted(lines)

  f = open(passedfile, 'w')
  dump_matrix(lines, passed, f)
  f.close()

  f = open(failedfile, 'w')
  dump_matrix(lines, failed, f)
  f.close()
