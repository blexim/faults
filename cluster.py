#!/usr/bin/python

import gzip
import cPickle
import os
import numpy
import scipy.cluster.hierarchy as hcluster
import metrics_suite

thresh = 1.2
metricname = 'euclidean'

def collect(metricnames, scores, res, cumulative):
  for s in scores:
    for (m, (l, (sworst, sbest, savg))) in zip(metricnames, s):
      if l > 0:
        normalised = float(savg) / l
      else:
        normalised = 0

      if normalised < 0:
        normalised = 0

      if m not in res:
        res[m] = [normalised]
        cumulative[m] = (1, normalised)
      else:
        res[m].append(normalised)
        (n, cum) = cumulative[m]
        cumulative[m] = (n + 1, cum + normalised)

def load_evaluations(evaldir, metricnames):
  res = {}
  cumulative = {}
  benchnames = []

  for d in os.listdir(evaldir):
    benchnames.append(d)

    fname = os.path.join(evaldir, d, 'evaluation')
    summaryf = gzip.GzipFile(fname, 'rb')
    scores = cPickle.load(summaryf)
    summaryf.close()

    collect(metricnames, scores, res, cumulative)

  return (res, cumulative)

def cluster(res):
  data = res.values()

  clusters = hcluster.fclusterdata(data, thresh, metric=metricname)

  clustered = {}

  for (m, c) in zip(res.keys(), clusters):
    if c not in clustered:
      clustered[c] = [m]
    else:
      clustered[c].append(m)

  return clustered.values()

def print_clusters(clusters, cumulative):
  i = 1

  for c in clusters:
    print "Cluster %d:" % i
    i += 1

    for m in c:
      (n, cum) = cumulative[m]
      score = (cum / n) * 100.0
      print "%s: %.02f" % (m, score)

    print ""

if __name__ == '__main__':
  import sys

  evaldir = sys.argv[1]

  if len(sys.argv) > 2:
    thresh = float(sys.argv[2])

  if len(sys.argv) > 3:
    metricname = sys.argv[3]

  metricnames = metrics_suite.suite.keys()

  (evals, cumulative) = load_evaluations(evaldir, metricnames)
  clusters = cluster(evals)
  print_clusters(clusters, cumulative)
