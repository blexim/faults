#!/usr/bin/python

import gzip
import cPickle
import os

def collect_summary(summary, res):
  for (m, r) in summary.iteritems():
    mean = (0.0 + sum(r)) / len(r)

    if m not in res:
      res[m] = []

    res[m].append(mean)

def collect_all_summaries(summarydir):
  res = {}
  benchnames = []

  for d in os.listdir(summarydir):
    benchnames.append(d)

    fname = os.path.join(summarydir, d, 'summary')
    summaryf = gzip.GzipFile(fname, 'rb')
    summary = cPickle.load(summaryf)
    summaryf.close()

    collect_summary(summary, res)

  return (benchnames, res)

def print_table(benchnames, res, tablef):
  tablef.write(r"\begin{tabular}{l|")

  for b in benchnames:
    tablef.write("|c")

  tablef.write("}\n")

  for b in benchnames:
    tablef.write("& %s" % b)

  tablef.write(r"\\")
  tablef.write("\n")
  tablef.write("\\hline\\hline\n")

  for (name, stats) in res.iteritems():
    tablef.write(name.replace('_', ' '))

    for s in stats:
      tablef.write("& %.02f" % s)

    tablef.write(r"\\")
    tablef.write("\n")

  tablef.write("\end{tabular}")

def make_table(summarydir, tablename):
  (benchnames, res) = collect_all_summaries(summarydir)

  tablef = open(tablename, 'w')
  print_table(benchnames, res, tablef)
  tablef.close()

if __name__ == '__main__':
  import sys

  summarydir = sys.argv[1]
  tablename = sys.argv[2]

  make_table(summarydir, tablename)
