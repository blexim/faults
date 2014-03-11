#!/usr/bin/python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import util
import metrics_suite
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

def plot_scores(scores, num_metrics):
  colours = iter(cm.rainbow(np.linspace(0, 1, num_metrics)))
  plots = []
  legends = []
  plotted = 0
  maxbugs = 0
  maxtries = 0
  mintries = 99999999
  ax = plt.subplot(1, 1, 1)
  #plt.yscale('log')
  #plt.xscale('log')

  for m in scores:
    if plotted == num_metrics:
      break

    plotted += 1

    linesexamined = sorted(scores[m])
    c = next(colours)

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
      plt.plot(xs, ys, '^', color=c, label=m)
    else:
      plt.plot(xs, ys, color=c, label=m)

  print "Plotted %d metrics" % plotted
  
  plt.xlabel("Bugs found")
  plt.ylabel("Lines examined")
  #ax.legend(loc=2)
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

  metricnames = [m for m in metrics_suite.suite.keys()
                 if not m.startswith('Prob_') and
                    not m.startswith('Just_') and
                    m != ('Const')]

  for fname in sys.argv[1:]:
    load_scores(fname, metricnames, scores)

  plot_scores(avg_scores, len(metricnames))
