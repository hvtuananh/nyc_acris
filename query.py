#!/usr/bin/python

import sys
from bbl import BBLQuery

try:
    borough = int(sys.argv[1])
    block = int(sys.argv[2])
    lot = int(sys.argv[3])
except:
    borough = 4
    block = 3631
    lot = 57 # Or 55, 53
    
#Another example: 1 1654 27

bbl_query = BBLQuery('localhost', 40000)
lots = bbl_query.query_lots(borough, block)

for idx, lot in enumerate(sorted(lots)):
    print "Running", idx, "of", len(lots), "..."
    bbl_query.query_bbl(borough, block, lot)