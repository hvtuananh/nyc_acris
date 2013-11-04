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
real	5m22.290s
user	0m0.125s
sys	0m0.072s
'''

#STEP2: 