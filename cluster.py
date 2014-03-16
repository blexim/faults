#!/usr/bin/python

import gzip
import cPickle
import os
import numpy
import scipy.cluster.hierarchy as hcluster
import scipy.stats

from util import load, is_measure
import metrics_suite

thresh = 1.1
metricname = 'cityblock'

pthresh = 0.01

def collect(metricnames, scores, res, cumulative):
  for s in scores:
    for (m, (l, (sworst, sbest, savg))) in zip(metricnames, s):
      if l > 0:
        x = float(savg)
        normalised = x / l
      else:
        continue

      if x < 0:
        continue

      if m not in res:
        res[m] = [x]
        cumulative[m] = (1, normalised)
      else:
        res[m].append(x)
        (n, cum) = cumulative[m]
        cumulative[m] = (n + 1, cum + normalised)

def load_evaluations(evalfs, metricnames):
  res = {}
  cumulative = {}
  benchnames = []

  for fname in evalfs:
    try:
      scores = load(fname)
    except:
      continue

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

def mean(xs):
  return sum(xs) / len(xs)

def find_better(evals, m):
  baseline = evals[m]
  better = []
  worse = []
  same = []

  for (k, vs) in evals.iteritems():
    if not is_measure(k):
      continue

    diff = compare(baseline, vs)
    x = mean(vs) * 100

    if diff == 0:
      same.append((x, k))
    elif diff > 0:
      better.append((x, k))
    else:
      worse.append((x, k))

  return (better, same, worse)

def print_better(m, cumulative, better, same, worse):
  print "BETTER than %s (%d):" % (m, len(better))
  for (x, n) in sorted(better):
    (k, z) = cumulative[n]
    score = (z / k) * 100
    print "%s %.02f%%" % (n, score)

  print "\nWORSE than %s (%d):" % (m, len(worse))
  for (x, n) in sorted(worse):
    (k, z) = cumulative[n]
    score = (z / k) * 100
    print "%s %.02f%%" % (n, score)

  print "\nTHE SAME as %s (%d):" % (m, len(same))
  for (x, n) in sorted(same):
    (k, z) = cumulative[n]
    score = (z / k) * 100
    print "%s %.02f%%" % (n, score)

def split_hypothesis(evalfs, m):
  metricnames = metrics_suite.suite.keys()
  (evals, cumulative) = load_evaluations(evalfs, metricnames)
  return (cumulative, find_better(evals, m))

if __name__ == '__main__':
  import sys

  evalfs = sys.argv[1:]

  (cumulative, (better, same, worse)) = split_hypothesis(evalfs, "Rand")
  print_better("Rand", cumulative, better, same, worse)
