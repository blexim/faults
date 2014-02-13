#!/usr/bin/python

import re
import cPickle
import gzip
import metrics
import metrics_suite

def do_stats(test_results, metric):
  fail_counts = {}
  pass_counts = {}
  total_failures = 0
  total_successes = 0

  for (correct, features) in test_results:
    if correct:
      total_successes += 1
      target = fail_counts
    else:
      total_failures += 1
      target = pass_counts

    for f in features:
      if f not in target:
        target[f] = 0

      target[f] += 1

  stats = []

  for i in fail_counts:
    failures = float(fail_counts[i])

    if i in pass_counts:
      successes = float(pass_counts[i])
    else:
      successes = 0

    suspiciousness = metric(failures, total_failures, successes, total_successes)
    stats.append((i, suspiciousness))

  return stats

def rank(stats):
  return sorted([(stat, line) for (line, stat) in stats])

def print_stats(ranked):
  for (stat, line) in ranked:
    print "%d: %f" % (line, stat)

def score(ranked, bugs):
  seen = set([])
  score = 0
  last_stat = 0.0

  bugs = set(l for (s, l) in ranked if l in bugs)

  for (s, l) in ranked:
    score += 1

    if l in bugs:
      seen.add(l)
      last_stat = s

    if len(seen) == len(bugs) and s != last_stat:
      return score-1

  return score

if __name__ == '__main__':
  import sys

  features = sys.argv[1]
  metric_name = sys.argv[2]

  f = gzip.GzipFile(features, 'rb')
  (bugs, test_results) = cPickle.load(f)
  f.close()

  metric = metrics_suite.suite[metric_name]

  stats = do_stats(test_results, metric)
  ranked = rank(stats)
  print_stats(ranked)
  print bugs
  print "Score: %d" % score(ranked, bugs)
