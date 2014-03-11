#!/usr/bin/python

import gzip
import cPickle

def load(fname):
  f = gzip.GzipFile(fname, 'rb')
  ret = cPickle.load(f)
  f.close()
  return ret

def save(o, fname):
  f = gzip.GzipFile(fname, 'wb')
  cPickle.dump(o, f, -1)
  f.close()

def is_measure(m):
  return not (m.startswith('Prob_') or
              m.startswith('Just_') or
              m == 'Const')
