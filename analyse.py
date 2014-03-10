#!/usr/bin/pypy

import re
import cPickle
import gzip
import metrics
import metrics_suite

WORST=0
BEST=1
AVG=2

lines = -1

def do_stats(test_results, metric):
  fail_counts = {}
  pass_counts = {}
  total_failures = 0
  total_successes = 0

  # Do we dedupe or not?...
  #reses = set((c, tuple(f)) for (c, f) in test_results)
  reses = test_results
  i = -1

  for (correct, features) in reses:
    i += 1

    if not features:
      continue

    if correct:
      total_successes += 1
      target = pass_counts
    else:
      total_failures += 1
      target = fail_counts

    for f in features:
      if f not in target:
        target[f] = 0

      target[f] += 1

  stats = []
  executed = set(fail_counts.keys())

  #print "Failed: %d, succeeded: %d" % (total_failures, total_successes)

  for i in executed:
    if i in fail_counts:
      failures = float(fail_counts[i])
    else:
      failures = 0.0

    if i in pass_counts:
      successes = float(pass_counts[i])
    else:
      successes = 0.0


    cf = float(failures)
    nf = float(total_failures - cf)
    cp = float(successes)
    np = float(total_successes - cp)

    suspiciousness = metric(cf, nf, cp, np)
    stats.append((i, suspiciousness))

  return stats

def rank(stats):
  return sorted([(stat, line) for (line, stat) in stats], reverse=True)

def print_stats(ranked):
  for (stat, line) in ranked:
    print "%d: %f" % (line, stat)

def score(ranked, bugs, score_type=WORST):
  ordinals = make_ordinals(ranked, score_type)
  bug_ordinals = [ordinals[b] for b in bugs if b in ordinals]

  if len(bug_ordinals) > 0:
    return min(bug_ordinals)
  else:
    return -1

def score_rand(ranked, bugs, score_type):
  if not [b for b in bugs if b in ranked]:
    return -1

  return len(ranked) / (len(bugs) + 1)

def make_ordinals(ranked, score_type=WORST):
  ret = {}
  i = 0
  n = 0
  last_s = None
  equal_s = []

  for (s, l) in ranked:
    if s != last_s:
      if score_type == WORST:
        ordinal = n + len(equal_s)
      elif score_type == BEST:
        ordinal = n
      elif score_type == AVG:
        ordinal = n + len(equal_s)/2

      for x in equal_s:
        ret[x] = ordinal

      n += len(equal_s)
      equal_s = []

    equal_s.append(l)
    last_s = s

  # Mop up last class...
  if score_type == WORST:
    ordinal = n + len(equal_s)
  elif score_type == BEST:
    ordinal = n
  elif score_type == AVG:
    ordinal = n + len(equal_s)/2

  for x in equal_s:
    ret[x] = ordinal

  return ret

def evaluate_metric(test_results, bugs, metric, score_type=WORST):
  stats = do_stats(test_results, metric)
  ranked = rank(stats)

  if len(ranked) == 0:
    return (0, (-1, -1, -1))

  if metric == metrics.Rand:
    # Special case rand!
    scorefunc = score_rand
  else:
    scorefunc = score

  #scorefunc = score

  ret = tuple(scorefunc(ranked, bugs, score_type) for score_type in
      (WORST, BEST, AVG))

  return (len(ranked), ret)

if __name__ == '__main__':
  import sys

  features = sys.argv[1]

  f = gzip.GzipFile(features, 'rb')
  (bugs, test_results) = cPickle.load(f)
  f.close()

  metric_name = sys.argv[2]
  metric = metrics_suite.suite[metric_name]
  stats = do_stats(test_results, metric)

  ranked = rank(stats)
  print_stats(ranked)
  print bugs
  print "Score: %d/%d" % (score(ranked, bugs, AVG), len(ranked))

  print evaluate_metric(test_results, bugs, metric, WORST)
