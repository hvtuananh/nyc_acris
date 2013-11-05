#!/usr/bin/python

from building import Building
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

data = pickle.load(open('graphs.bin'))
graphs = dict()

for building in data:
    if not building:
        continue
    graphs[building.bbl] = building
    
pickle.dump(graphs, open('buildings.bin', 'w'))