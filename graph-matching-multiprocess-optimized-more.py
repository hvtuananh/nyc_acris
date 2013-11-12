#!/usr/bin/python

from building import Building
from bbl import BBL
import pickle
from multiprocessing import Process, Pool
import traceback
import time
import sys

borough = int(sys.argv[1])

def calculate_similarities(bbl):
    # Optimize #2: Only calculate for 1 borough
    if bbl.borough != borough:
        return None
    start = time.clock()
    results = dict()
    target = buildings[bbl]
    for k,v in buildings.iteritems():
        # Optimize: Only need to calculate when target is less than v
        if target >= v:
            continue
        try:
            score = target.similarity(v)
            if score == 0:
                continue
            results[k] = score
        except:
            traceback.print_exc()
            print "This is an error!" + int(1)
    
    print time.clock() - start, bbl        
    return (bbl, results)

buildings = pickle.load(open('buildings.bin'))

#1. Compose a list of BBL:
bbls = buildings.keys()

pool = Pool(processes=60)
results = pool.map(calculate_similarities, bbls)

pickle.dump(results, open('match-scores-optimized-more-'+str(borough)+'.bin','w'))