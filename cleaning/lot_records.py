#!/usr/bin/python

'''
This script filter all BBL in lot_records before adding it to database
'''

import csv
import pickle

reader = csv.reader(open('data/acris/ACRIS_LotRecords.csv'), delimiter='|')
writer = csv.writer(open('data/acris/lot_records.csv', 'w'))
bbls_keep = pickle.load(open('pluto.bin'))

header = ['Unique_Key','Record_type','Borough','Block','Lot','Easement','Partial_lot','Air_rights','Subterranean_rights','Property_type','Street_number','Street_name','Addr_unit']
writer.writerow(header)

unique_keys = set()

for row in reader:
    borough = int(row[header.index('Borough')])
    block = int(row[header.index('Block')])
    lot = int(row[header.index('Lot')])
    bbl = long(borough*1000000000+block*10000+lot)
    if bbl not in bbls_keep:
        continue
    
    if row[header.index('Unique_Key')] != '':
        unique_keys.add(long(row[header.index('Unique_Key')]))
        
    writer.writerow(row)
    
pickle.dump(unique_keys, open('unique_keys.bin', 'w'))
fkey = open('unique_keys.txt','w')
for key in unique_keys:
    fkey.write(str(key) + '\n')