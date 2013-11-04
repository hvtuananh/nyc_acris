#!/usr/bin/python

'''
This script discarded all BBL following a specific rules
'''

from pymongo import MongoClient
import pickle
import re

client = MongoClient('localhost', 40002)
db = client.furman

fbbl = open('pluto.txt', 'w')
bbls = set()
bbl_records = list(db.pluto.find({'$or':[{'UnitsRes':{'$lte':3}},{'BldgClass':'C6'},{'BldgClass':'C8'},{'BldgClass':'D0'},{'BldgClass':'D4'},{'BldgClass':{'$regex':'^R'}}]}, {'BBL':1}))
for bbl_record in bbl_records:
    if bbl_record['BBL'] == '':
        continue
    bbls.add(bbl_record['BBL'])

bbls_all = set()
bbl_records = list(db.pluto.find({}, {'BBL':1}))
for bbl_record in bbl_records:
    if bbl_record['BBL'] == '':
        continue
    bbls_all.add(bbl_record['BBL'])

bbls_keep = bbls_all.difference(bbls)
for bbl in bbls_keep:
    fbbl.write(str(bbl)+'\n')
fbbl.flush()

pickle.dump(bbls_keep, open('pluto.bin', 'w'))