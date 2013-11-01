#!/usr/bin/python

'''
This script will query for all statistic available in our database, regardless of it's situation
'''

from pymongo import MongoClient
import pickle

client = MongoClient('localhost', 40000)
db = client.furman

primary = dict()
secondary = dict()
party_records = db.party_records.find({}, {'name_unified':1, 'party_type':1})
for party_record in party_records:
    if party_record['party_type'] == 1:
        try:
            secondary[party_record['name_unified']] += 1
        except:
            secondary[party_record['name_unified']] = 1
    
    if party_record['party_type'] == 2:
        try:
            primary[party_record['name_unified']] += 1
        except:
            primary[party_record['name_unified']] = 1
            
pickle.dump(primary, open('primary.txt', 'w'))
pickle.dump(secondary, open('secondary.txt', 'w'))