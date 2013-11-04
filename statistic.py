#!/usr/bin/python

'''
This script will query for all statistic available in our database, regardless of it's situation
'''

from pymongo import MongoClient
import pickle

client = MongoClient('localhost', 40002)
db = client.furman

primary = dict()
secondary = dict()
party_records = db.party_records.find({}, {'NameUnified':1, 'Party_type':1, 'Addr1Unified':1, 'Addr2Unified':1, 'Zip':1})
for party_record in party_records:
    try:
        key = party_record['NameUnified'] + party_record['Addr1Unified'] + party_record['Addr2Unified'] + str(party_record['Zip'])
    except:
        continue
        
    if party_record['Party_type'] == 1:
        try:
            secondary[key] += 1
        except:
            secondary[key] = 1
    
    if party_record['Party_type'] == 2:
        try:
            primary[key] += 1
        except:
            primary[key] = 1
            
pickle.dump(primary, open('primary.txt', 'w'))
pickle.dump(secondary, open('secondary.txt', 'w'))