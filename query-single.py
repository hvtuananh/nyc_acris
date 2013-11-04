#!/usr/bin/python

import sys
from bbl import BBL
from bbl_query import BBLQuery

try:
    borough = int(sys.argv[1])
    block = int(sys.argv[2])
    lot = int(sys.argv[3])
except:
    borough = 3
    block = 3430
    lot = 41 # Or 55, 53
    
#Another example: 1 1654 27

bblquery = BBLQuery('localhost', 40002)
lots = list([lot])

for idx, lot in enumerate(sorted(lots)):
    print "Running", idx, "of", len(lots), "..."
    building = bblquery.query_bbl(BBL(borough, block, lot))
    print building