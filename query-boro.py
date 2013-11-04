#!/usr/bin/python

import sys
from bbl import BBL
from bbl_query import BBLQuery

try:
    borough = int(sys.argv[1])
except:
    borough = 3

bblquery = BBLQuery('localhost', 40002)
blocks = bblquery.get_blocks(borough)

print blocks