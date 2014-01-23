#!/usr/bin/python

import re
import cPickle

line_taken_re = '^\s*(\d+):\s*(\d+):'
line_taken = re.compile(line_taken_re)

def coverage(gcov_data):
  ret = {}

  for l in gcov_data.split('\n'):
    taken = line_taken.match(l)

    if taken:
      times = int(taken.group(1))
      lineno = int(taken.group(2))

      if times > 0:
        ret[lineno] = True

  ret = tuple(sorted(ret))
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

def do_stats(passed, failed):
  counts = {}

  for features in failed:
    for feature in features:
      if feature not in counts:
        counts[feature] = 0

      counts[feature] += 10

  for features in passed:
    for feature in features:
      if feature not in counts:
        counts[feature] = 0

      counts[feature] -= 1

  return counts

def print_stats(stats):
  lines = sorted([(count, line) for (line, count) in stats.items()],
                 reverse = True)

  for (count, line) in lines:
    print "%d: %d" % (line, count)


if __name__ == '__main__':
  import sys

  golden = sys.argv[1]
  mutated = sys.argv[2]

  results = analyse_tests(golden, mutated)
  stats = do_stats(*results)
  print_stats(stats)
