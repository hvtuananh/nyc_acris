#!/usr/bin/python

'''
This script filter all BBL in lot_records before adding it to database
'''

import csv
import pickle
import sys
csv.field_size_limit(sys.maxsize)

reader = csv.reader(open('data/acris/ACRIS_PartyRecords.csv'), delimiter='|')
writer = csv.writer(open('data/acris/party_records.csv', 'w'))
keys_keep = pickle.load(open('unique_keys.bin'))

header = ['Unique_Key','Record_type','Party_type','Name','NameUnified','Addr1','Addr1Unified','Addr2','Addr2Unified','Country','City','State','Zip']
writer.writerow(header)

unique_keys = set()

for row in reader:
    try:
        key = long(row[header.index('Unique_Key')])
    except:
        continue
        
    if key not in keys_keep:
        continue
        
    writer.writerow(row)