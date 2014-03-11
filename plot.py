#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import util
import metrics_suite
import cluster
from analyse import WORST, BEST, AVG

def load_scores(fname, metricnames, scores):
  evals = util.load(fname)

  for benchmark in evals:
    for i in xrange(len(metricnames)):
      m = metricnames[i]
      metric_scores = benchmark[i]

      numlines = metric_scores[0]
      all_scores = metric_scores[1]
      (worst_score, best_score, avg_score) = all_scores

      for (score, scoredict) in zip(all_scores, scores):
        if m not in scoredict:
          scoredict[m] = [score]
        else:
          scoredict[m].append(score)

def plot_scores(scores, split, num_metrics):
  (better, same, worse) = split
  plots = []
  legends = []
  plotted = 0
  maxbugs = 0
  maxtries = 0
  mintries = 99999999
  ax = plt.subplot(1, 1, 1)
  #plt.yscale('log')
  #plt.xscale('log')

  better = [m for (_, m) in better]
  same = [m for (_, m) in same]
  worse = [m for (_, m) in worse]

  better_colour = '#079100'
  same_colour = '#e3b009'
  worse_colour = '#fc1414'

  better_style = ':'
  same_style = '-'
  worse_style = '--'

  labels = set([])

  for m in scores:
    if plotted == num_metrics:
      break

    if not util.is_measure(m):
      continue

    plotted += 1

    linesexamined = sorted(scores[m])

    if m in better:
      c = better_colour
      s = better_style
      label = "Better than random"
    elif m in same:
      c = same_colour
      s = same_style
      label = "Same as random"
    elif m in worse:
      c = worse_colour
      s = worse_style
      label = "Worse than random"
    else:
      print m

    if m == 'Rand':
      label = "Random"
    elif m == 'Lex':
      label = 'Lex'

    if label in labels:
      label = ""

    labels.add(label)

    xs = [0]
    ys = [0]
    total = 1
    i = 0

    for l in linesexamined:
      if l <= 0:
        continue

      total += l
      i += 1

      xs.append(i)
      ys.append(total)

    maxtries = max(maxtries, total)
    mintries = min(mintries, total)
    maxbugs = max(maxbugs, i)

    if m == 'Rand':
      plt.plot(xs, ys, 'o', color=c, label=m)
    elif m == 'Lex':
      plt.plot(xs, ys, 'd', color=c, label=m)
    else:
      plt.plot(xs, ys, s, color=c, label=label)

  print "Plotted %d metrics" % plotted
  
  plt.xlabel("Bugs found")
  plt.ylabel("Lines examined")
  ax.legend(loc=2)
  ax.set_xlim(0, maxbugs)
  ax.set_ylim(0, mintries)
  plt.savefig("sfl-cactus-avg-fill-space.pdf")
  plt.show()

if __name__ == '__main__':
  import sys

  worst_scores = {}
  best_scores = {}
  avg_scores = {}
  scores = (worst_scores, best_scores, avg_scores)

  metricnames = metrics_suite.suite.keys()

  evalfs = sys.argv[1:]

  for fname in evalfs:
    load_scores(fname, metricnames, scores)

  (_, split) = cluster.split_hypothesis(evalfs, "Rand")

  plot_scores(avg_scores, split, len(metricnames))
