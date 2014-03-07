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
lines = 173

def collect(metricnames, scores, res, cumulative):
  for s in scores:
    for (m, (l, (sworst, sbest, savg))) in zip(metricnames, s):
      if l > 0:
        normalised = float(savg) / lines
      else:
        continue

      if normalised < 0:
        continue

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

  fname = os.path.join(evaldir, 'evaluation')
  summaryf = gzip.GzipFile(fname, 'rb')
  scores = cPickle.load(summaryf)
  summaryf.close()

  collect(metricnames, scores, res, cumulative)

  return (res, cumulative)

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

def print_res(cumulative):
  for (m, (n, s)) in cumulative.iteritems():
    x = (s/n) * 100
    print "%s: %.02f%%" % (m, x)

if __name__ == '__main__':
  import sys

  evaldir = sys.argv[1]

  if len(sys.argv) > 2:
    thresh = float(sys.argv[2])

  if len(sys.argv) > 3:
    metricname = sys.argv[3]

  metricnames = metrics_suite.suite.keys()

  (evals, cumulative) = load_evaluations(evaldir, metricnames)
  print_res(cumulative)

  print len(evals)
