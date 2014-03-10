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
