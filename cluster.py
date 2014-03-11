#!/usr/bin/python

import gzip
import cPickle
import os
import numpy
import scipy.cluster.hierarchy as hcluster
import scipy.stats

from util import load
import metrics_suite

thresh = 1.1
metricname = 'cityblock'

pthresh = 0.01

def collect(metricnames, scores, res, cumulative):
  for s in scores:
    for (m, (l, (sworst, sbest, savg))) in zip(metricnames, s):
      if l > 0:
        normalised = float(savg) / l
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
    diff = compare(baseline, vs)
    x = mean(vs) * 100

    if diff == 0:
      same.append((x, k))
    elif diff > 0:
      better.append((x, k))
    else:
      worse.append((x, k))

  print "BETTER than %s (%d):" % (m, len(better))
  for (x, n) in sorted(better):
    print "%s %.02f%%" % (n, x)


  print "\nWORSE than %s (%d):" % (m, len(worse))
  for (x, n) in sorted(worse):
    print "%s %.02f%%" % (n, x)

  print "\nTHE SAME as %s (%d):" % (m, len(same))
  for (x, n) in sorted(same):
    print "%s %.02f%%" % (n, x)

if __name__ == '__main__':
  import sys

  evaldir = sys.argv[1]

  if len(sys.argv) > 2:
    thresh = float(sys.argv[2])

  if len(sys.argv) > 3:
    metricname = sys.argv[3]

  metricnames = [m for m in metrics_suite.suite.keys() if
                 not m.startswith('Prob_') and
                 not m.startswith('Just_') and
                 m != ('Const')]

  (evals, cumulative) = load_evaluations(evaldir, metricnames)
  #clusters = cluster(evals)
  #print_clusters(clusters, cumulative)

  find_better(evals, "Rand")

  print len(evals)
