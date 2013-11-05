#!/usr/bin/python

import sys
from bbl import BBL
from bbl_query import BBLQuery
from multiprocessing import Process, Pool
import pickle
import traceback
import sys

def query_bbl(block):
    buildings = set()
    bbls = bblquery.get_bbls(BBL(borough, block, 1))
    for idx, bbl in enumerate(sorted(bbls)):
        print "Running", idx, "of", len(bbls), "..."
        try:
            building = bblquery.query_bbl(bbl)
        except:
            traceback.print_exc()
            print "Error" + 10 + "!"
        buildings.add(building)
        
    pickle.dump(buildings, open('blocks/' + str(block), 'w'))

try:
    borough = int(sys.argv[1])
except:
    borough = 3
    

bblquery = BBLQuery('localhost', 40002)
blocks = bblquery.get_blocks(borough)
pool = Pool(processes=32)
pool.map(query_bbl, blocks)