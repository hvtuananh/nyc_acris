#!/usr/bin/python

'''
This script will clean unused records in our database, keeps it small and easier to query
'''

from pymongo import MongoClient
import pickle
import re

client = MongoClient('localhost', 40000)
db = client.furman

#STEP1: Remove all BK_ and FT_ records
'''
regex1 = re.compile(r'^FT_|^BK_')

print "Cleaning lot_records..."
db.lot_records.remove({'key':regex1})
db.lot_records.remove({'key':regex1})

print "Cleaning master_records..."
db.master_records.remove({'key':regex1})
db.master_records.remove({'key':regex1})

print "Cleaning party_records..."
db.party_records.remove({'key':regex1})
db.party_records.remove({'key':regex1})

print "Cleaning remarks_records..."
db.remarks_records.remove({'key':regex1})
db.remarks_records.remove({'key':regex1})
'''
'''
real	5m22.290s
user	0m0.125s
sys	0m0.072s
'''

#STEP2: How to remove BBL properly in PLUTO?
#First, get all BBLs according to the query:
fbbl = open('bbls.txt', 'w')
fkey = open('keys.txt', 'w')

bbls = db.pluto.find({'$or':[{'UnitsRes':{'$lte':3}},{'BldgClass':'C6'},{'BldgClass':'C8'},{'BldgClass':'D0'},{'BldgClass':'D4'},{'BldgClass':{'$regex':'^R'}}]}, {'BBL':1,'BoroCode':1,'Block':1,'Lot':1})
for bbl in bbls:
    fbbl.write(str(bbl['BBL']) + '\n')
    fbbl.flush()
    
    #Drop data in PLUTO
    db.pluto.remove({'BBL':bbl['BBL']})
    
    
    #Query Lots
    lots = db.lot_records.find({'borough':bbl['BoroCode'],'block':bbl['Block'],'lot':bbl['Lot']},{'key':1})
    unique_keys = set()
    for lot in lots:
        unique_keys.add(lot['key'])
    if len(unique_keys) == 0:
        continue
    for key in unique_keys:
        fkey.write(str(key) + '\n')
    fkey.flush()
    
    unique_keys = list(unique_keys)
    
    #Drop data in ACRIS:
    db.lot_records.remove({'key':{'$in': unique_keys}})
    db.master_records.remove({'key':{'$in': unique_keys}})
    db.party_records.remove({'key':{'$in': unique_keys}})