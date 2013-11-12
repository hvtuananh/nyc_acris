#!/usr/bin/python

import pickle
import sys

data = pickle.load(open('match-scores-optimized-more-4.bin'))
data = filter(None, data)

# 1. Construct full graph from pickle
graph = dict()
for (k,v) in data:
    for x,y in v.iteritems():
        # Need to do full construction for better lookup
        graph[(k,x)] = y
        # Actually don't need since we already know the order of BBL
        #graph[(x,k)] = y

# 2b. Test merging function
'''
graph = {
    (1,2):1,
    (3,4):1,
    (5,6):1,
    (7,8):1,
    (1,8):1,
    (4,5):1,
    (1,4):1
}
'''

results = list()        
for k,v in sorted(graph.iteritems(), key=lambda(k,v):(v,k), reverse=True):
    if v < 0.5: break
    done = False
    anchor_set = None
    for x in results:
        if k[0] in x or k[1] in x:
            if not done:
                x.add(k[0])
                x.add(k[1])
                done = True
                anchor_set = x
            else:
                anchor_set |= x
                results.remove(x)
            
    if not done:
        x = set(k)
        results.append(x)
        
# 2. Convert list to set for deduplication
# Since this case might happen:
# a <-> b then c <-> d then a <-> c
        
for x in sorted(results, key=lambda s:len(s), reverse=False):
    print "\nThis group has", len(x), "BBLs"
    for y in x:
        sys.stdout.write(str(y) + '  ')
    sys.stdout.write("\n")
        