#!/usr/bin/python

import cluster
import metrics_suite

def is_best(evals, m):
  (better, same, worse) = cluster.find_better(evals, m)

  if not better:
    return True
  else:
    return False

def find_best(evalfs, metricnames):
  (evals, _) = cluster.load_evaluations(evalfs, metricnames)
  ret = []

  for m in metricnames:
    if is_best(evals, m):
      ret.append(m)

  return ret

if __name__ == '__main__':
  import sys

  evalfs = sys.argv[1:]
  metricnames = metrics_suite.suite.keys()

  print find_best(evalfs, metricnames)
