#!/usr/bin/python

import sys
sys.path.append('../../geoclient')
import pickle

from pymongo import MongoClient
client = MongoClient('localhost', 40002)
db = client.furman
addresses = dict()
parties = db.party_records.find({})
for party in parties:
    try:
        address = {
            'ACRIS_Addr1':party['Addr1'],
            'ACRIS_Addr2':party['Addr2'],
            'ACRIS_City':party['City'],
            'ACRIS_State':party['State'],
            'ACRIS_Zip':party['Zip'],
        }
        addr_hash = hash(str(address['ACRIS_Addr1']) + ',' + str(address['ACRIS_City']) + ',' + str(address['ACRIS_State']) + ',' + str(address['ACRIS_Zip']))
    except KeyError:
        continue
        
    addresses[addr_hash] = address
    
pickle.dump(addresses, open('addresses.bin', 'w'))