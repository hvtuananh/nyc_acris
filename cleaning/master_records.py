#!/usr/bin/python

'''
This script filter all BBL in lot_records before adding it to database
'''

import csv
import pickle

reader = csv.reader(open('data/acris/ACRIS_MasterRecords.csv'), delimiter='|')
writer = csv.writer(open('data/acris/master_records.csv', 'w'))
keys_keep = pickle.load(open('unique_keys.bin'))

header = ['Unique_Key','Record_type','Date_File_Created','CRFN','Recorded_borough','Doc_type','Document_Date','Document_amt','Recorded_datetime','Ucc_collateral','Fedtax_serial_nbr','Fedtax_assessment_date','Rpttl_nbr','Modified_date','Reel_yr','Reel_nbr','Reel_pg','File_nbr']
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