#!/usr/bin/python

import pickle, sys, os

input = sys.argv[1]
output = sys.argv[2]

buildings = set()
#for file in os.listdir(input):
for file in "bronx.bin  brooklyn.bin  manhattan.bin  queens.bin  stisland.bin".split():
    data = pickle.load(open(file))
    buildings |= data
    
pickle.dump(buildings, open(output, 'w'))