#!/usr/bin/python

import metrics
import metrics_suite

def Ensemble(cf, nf, cp, np):
  ret = 0

  for m in metrics_suite.suite.itervalues():
    ret += m(cf, nf, cp, np)

  return ret
