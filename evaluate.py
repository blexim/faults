#!/usr/bin/python

import metrics_suite
import analyse
import os
import gzip
import cPickle

def evaluate_all_metrics(featurefile, metrics):
  f = gzip.GzipFile(featurefile, 'rb')
  (bugs, test_results) = cPickle.load(f)
  f.close()

  ret = []

  for m in metrics:
    score = analyse.evaluate_metric(test_results, bugs, m, analyse.WORST)
    ret.append(score)

  return ret

def evaluate_on_benchmark(benchdir, metrics):
  benchnum = 1
  ret = []

  while os.path.isfile(os.path.join(benchdir, 'v%d' % benchnum)):
    f = os.path.join(benchdir, 'v%d' % benchnum)
    print f
    ret.append(evaluate_all_metrics(f, metrics))
    benchnum += 1

  return ret

def summarise(metricnames, res):
  ret = {m: 0.0 for m in metricnames}

  for r in res:
    for (m, x) in zip(metricnames, r):
      ret[m] += x

  for m in metricnames:
    ret[m] /= len(res)

  return ret

def print_summary(summary):
  for (m, x) in summary.iteritems():
    print "%s: %.02f%%" % (m, x)

if __name__ == '__main__':
  import sys

  benchdir = sys.argv[1]
  metrics = []
  metricnames = []

  for (n, m) in metrics_suite.suite.iteritems():
    metricnames.append(n)
    metrics.append(m)

  scores = evaluate_on_benchmark(benchdir, metrics)
  summary = summarise(metricnames, scores)
  print_summary(summary)
