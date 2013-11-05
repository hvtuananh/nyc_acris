#!/usr/bin/python

from building import Building
from bbl import BBL
import pickle
import sys

try:
    borough = int(sys.argv[1])
    block = int(sys.argv[2])
    lot = int(sys.argv[3])
except:
    borough = 3
    block = 3430
    lot = 41

buildings = pickle.load(open('buildings.bin'))
results = dict()
target = buildings[BBL(borough, block, lot)]
for k,v in buildings.iteritems():
    results[k] = target.similarity(v)
    
for k,v in sorted(results.iteritems(), key=lambda(k,v):(v,k), reverse=False):
    print k,v