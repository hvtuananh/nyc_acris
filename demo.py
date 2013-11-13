from bbl import BBL
import pickle
import sys
import json

data = list()
chunk = pickle.load(open('match-scores-optimized-more-1.bin'))
chunk = filter(None, chunk)
data += chunk
chunk = pickle.load(open('match-scores-optimized-more-2.bin'))
chunk = filter(None, chunk)
data += chunk
chunk = pickle.load(open('match-scores-optimized-more-3.bin'))
chunk = filter(None, chunk)
data += chunk
chunk = pickle.load(open('match-scores-optimized-more-4.bin'))
chunk = filter(None, chunk)
data += chunk

# 1. Construct full graph from pickle
graph = dict()
for (k,v) in data:
    for x,y in v.iteritems():
        # Need to do full construction for better lookup
        graph[(k,x)] = y
        # Actually don't need since we already know the order of BBL
        #graph[(x,k)] = y

bbls = "3-4648-33  3-5082-67  3-4898-4  3-1269-20  3-4598-1  3-1322-26  3-1418-49  3-1413-1  3-4633-1  3-5065-100  3-1388-53  3-1419-6  3-4615-41  3-1403-40  3-4668-20  3-4633-65  3-5105-43  3-1296-28  3-1425-13  3-1419-1".split()

json3 = list()
bbl_list = list()
for bbl_s in bbls:
    bbl_r = bbl_s.split('-')
    borough = int(bbl_r[0])
    block = int(bbl_r[1])
    lot = int(bbl_r[2])
    
    bbl_list.append(BBL(borough, block, lot))
    
    json4 = dict()
    json4['name'] = bbl_s
    json4['group'] = 1
    json3.append(json4)

json1 = list()
for x in bbl_list:
    for y in bbl_list:
        if x > y: continue
        if (x,y) in graph:
            if graph[(x,y)] < 1:
                continue
            json2 = dict()
            json2['source'] = bbl_list.index(x)
            json2['target'] = bbl_list.index(y)
            json2['value'] = graph[(x,y)]
            json1.append(json2)
           
json5 = {
    'nodes':json3,
    'links':json1
} 
            
print json.dumps(json5)