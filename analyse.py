#!/usr/bin/pypy

import re
import cPickle
import gzip
import metrics
import metrics_suite
import ensemble_metric

WORST=0
BEST=1
AVG=2

def do_stats(test_results, metric):
  fail_counts = {}
  pass_counts = {}
  total_failures = 0
  total_successes = 0

  # Do we dedupe or not?...
  #reses = set((c, tuple(f)) for (c, f) in test_results)
  reses = test_results

  for (correct, features) in reses:
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
  return sorted([(stat, line) for (line, stat) in stats], reverse=True)

def print_stats(ranked):
  for (stat, line) in ranked:
    print "%d: %f" % (line, stat)

def score(ranked, bugs, score_type=WORST):
  ordinals = make_ordinals(ranked, score_type)
  bug_ordinals = [ordinals[b] for b in bugs if b in ordinals]
  return max(bug_ordinals)

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

def ensemble_stats(test_results, metric_set, score_type=WORST):
  ensemble_ordinals = None

  for m in metric_set:
    stats = do_stats(test_results, m)
    ordinals = make_ordinals(rank(stats), score_type)

    if ensemble_ordinals is None:
      ensemble_ordinals = ordinals
    else:
      for l in ordinals:
        ensemble_ordinals[l] += ordinals[l]

  return [(l, ensemble_ordinals[l]) for l in ensemble_ordinals]

if __name__ == '__main__':
  import sys

  features = sys.argv[1]

  f = gzip.GzipFile(features, 'rb')
  (bugs, test_results) = cPickle.load(f)
  f.close()

  if len(sys.argv) > 2:
    metric_name = sys.argv[2]
    metric = metrics_suite.suite[metric_name]
    stats = do_stats(test_results, metric)
  else:
    stats = ensemble_stats(test_results,
        [metrics.Pearson3, metrics.Wong3], WORST)

  ranked = rank(stats)
  print_stats(ranked)
  print bugs
  print "Score: %d/%d" % (score(ranked, bugs), len(ranked))
