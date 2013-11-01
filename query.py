#!/usr/bin/python

import sys
from bbl import BBL
from bbl_query import BBLQuery

try:
    borough = int(sys.argv[1])
    block = int(sys.argv[2])
    lot = int(sys.argv[3])
except:
    borough = 4
    block = 3631
    lot = 57 # Or 55, 53
    
#Another example: 1 1654 27

bblquery = BBLQuery('localhost', 40000)
bbls = bblquery.get_bbls(BBL(borough, block, lot))

for idx, bbl in enumerate(sorted(bbls)):
    print "Running", idx, "of", len(bbls), "..."
    bblquery.query_bbl(bbl)