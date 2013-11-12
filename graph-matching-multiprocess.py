#!/usr/bin/python

from building import Building
from bbl import BBL
import pickle
from multiprocessing import Process, Pool
import traceback

def calculate_similarities(bbl):
    print bbl
    results = list()
    for other in bbls:
        try:
            results.append(calculate_similarity((bbl, other)))
        except:
            traceback.print_exc()
            print "This is an error!" + int(1)
    
def calculate_similarity(pairs):
    return buildings[pairs[0]].similarity(buildings[pairs[1]])

buildings = pickle.load(open('buildings.bin'))

#1. Compose a list of BBL:
bbls = buildings.keys()

pool = Pool(processes=60)
results = pool.map(calculate_similarities, bbls)

pickle.dump(results, open('match-scores.bin','w'))