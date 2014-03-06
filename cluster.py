#!/usr/bin/python

import gzip
import cPickle
import os
import numpy
import scipy.cluster.hierarchy as hcluster
import scipy.stats

import metrics_suite

thresh = 1.1
metricname = 'cityblock'

pthresh = 0.01

def collect(metricnames, scores, res, cumulative):
  for s in scores:
    for (m, (l, (sworst, sbest, savg))) in zip(metricnames, s):
      if l > 0:
        normalised = float(sworst) / l
      else:
        continue

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

def compare(m1, m2):
  (T, p) = scipy.stats.wilcoxon(m1, m2)

  if p <= pthresh:
    if sum(m1) > sum(m2):
      return p
    else:
      return -p

  return 0

def find_better(evals, m):
  baseline = evals[m]
  better = []
  worse = []
  same = []

  for (k, vs) in evals.iteritems():
    diff = compare(baseline, vs)

    if diff == 0:
      same.append(k)
    elif diff > 0:
      better.append(k)
    else:
      worse.append(k)

  print "BETTER than %s:" % m
  for n in better:
    print n


  print "\nWORSE than %s:" % m
  for n in worse:
    print n

  print "\nTHE SAME as %s:" % m
  for n in same:
    print n

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

  find_better(evals, "Rand")
