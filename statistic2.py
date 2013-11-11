#!/usr/bin/python

import pickle
from bbl import BBL
from building import Building

buildings = pickle.load(open('buildings.bin'))

primary = dict()
secondary = dict()
for k,v in buildings.iteritems():
    try:
        primary[v.primary] += 1
    except:
        primary[v.primary] = 1
    for owner in v.secondary:
        try:
            secondary[owner] += 1
        except:
            secondary[owner] = 1

print "Top 100 primary owners:"
count = 0
for k,v in sorted(primary.iteritems(), key=lambda(k,v):(v,k), reverse=True):
    count += 1
    print k['name'], v
    if count > 100:
        break
        
print "Top 100 secondary owners:"
count = 0
for k,v in sorted(secondary.iteritems(), key=lambda(k,v):(v,k), reverse=True):
    count += 1
    print k['name'], v
    if count > 100:
        break