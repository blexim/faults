#!/usr/bin/pypy

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
  ret = {}

  for i in xrange(len(metricnames)):
    m = metricnames[i]
    ret[m] = [float(r[i][1][0]) / r[i][0] for r in res if r[i][0] > 0 and r[i][1][0] > 0]

  return ret

def print_summary(summary):
  res = []

  for (m, rs) in summary.iteritems():
    mean = (0.0 + sum(rs)) / len(rs)
    res.append((mean, m))

  res.sort()

  for (x, m) in res:
    print "%s: %.02f" % (m, x)

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

  evaluation = (metricnames, scores)

  evaluatef = os.path.join(benchdir, 'evaluation')
  f = gzip.GzipFile(evaluatef, 'wb')
  cPickle.dump(scores, f, -1)
  f.close()

  summaryf = os.path.join(benchdir, 'summary')
  f = gzip.GzipFile(summaryf, 'wb')
  cPickle.dump(summary, f, -1)
  f.close()
