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
  fail_counts = {}
  pass_counts = {}

  for features in failed:
    for feature in features:
      if feature not in fail_counts:
        fail_counts[feature] = 1

      fail_counts[feature] += 1


  for features in passed:
    for feature in features:
      if feature not in pass_counts:
        pass_counts[feature] = 1

      pass_counts[feature] += 1

  stats = []

  for i in fail_counts:
    failures = float(fail_counts[i])
    successes = float(pass_counts[i])

    # CHANGE THIS LINE vvv
    suspiciousness = failures**2 / successes
    # THAT ONE ^^^

    stats.append((i, suspiciousness))

  return stats

def print_stats(stats):
  lines = sorted([(stat, line) for (line, stat) in stats],
                 reverse = True)

  for (stat, line) in lines:
    print "%d: %f" % (line, stat)


if __name__ == '__main__':
  import sys

  golden = sys.argv[1]
  mutated = sys.argv[2]

  results = analyse_tests(golden, mutated)
  stats = do_stats(*results)
  print_stats(stats)
