from bbl import BBL
import pickle
import sys
import json

data = list()
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

bbls = "3-3326-34  3-3166-41  3-3294-42  3-3326-48  3-3166-52  3-3441-5  3-3247-40  3-3269-52  3-3279-43  3-3217-18  3-3186-18  3-3283-8  3-3393-43  3-3314-35  3-3187-21  3-3188-7  3-3266-40  3-3187-28  3-3266-45  3-3444-16  3-3173-3  3-3236-20  3-3301-5  3-3236-22  3-3219-47  3-3187-48  3-3384-16  3-3173-22  3-3220-40  3-3171-59  3-3220-44  3-3332-47  3-3301-32  3-3333-33  3-3269-35  3-3447-5  3-3297-51  3-3175-11  3-3175-15  3-3157-52  3-3320-9  3-3175-26  3-3174-44  3-3430-46  3-3175-32  3-3151-163  3-3287-38  3-3257-12  3-3177-13  3-3219-21  3-3209-17  3-3289-19  3-3289-21  3-3177-12  3-3220-51  3-3211-4  3-3257-43  3-3322-28  3-3188-40  3-3211-33  3-3258-50  3-3197-11  3-3291-46  3-3165-23  3-3436-18  3-3183-37  3-3309-2  3-3246-16  3-3311-4  3-3166-23  3-3326-26  3-3151-12  3-3326-29".split()

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
            json2 = dict()
            json2['source'] = str(x)
            json2['target'] = str(y)
            json2['value'] = graph[(x,y)]
            json1.append(json2)
           
json5 = {
    'nodes':json3,
    'links':json1
} 
            
print json.dumps(json5)