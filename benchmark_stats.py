#!/usr/bin/pypy

from util import load

def load_features(featurefile):
  (bugs, test_results) = load(featurefile)
  executed = set([])
  bugs = set(bugs)

  for (_, features) in test_results:
    executed.update(features)

  num_bugs = len(bugs)
  num_execed_bugs = len(bugs.intersection(executed))

  return (num_bugs, num_execed_bugs)

def feature_stats(files):
  not_execd = 0
  bug_counts = {b: 0 for b in xrange(100)}

  for f in files:
    (num_bugs, num_execd) = load_features(f)

    bug_counts[num_execd] += 1

  return bug_counts

def print_summary(bug_counts):
  for b in sorted(bug_counts.keys()):
    if bug_counts[b]:
      print "%d bugs: %d" % (b, bug_counts[b])

if __name__ == '__main__':
  import sys

  files = sys.argv[1:]

  counts = feature_stats(files)
  print_summary(counts)
