#!/usr/bin/python

'''
This script filter all BBL in lot_records before adding it to database
'''

import csv
import pickle
import sys
csv.field_size_limit(sys.maxsize)

reader = csv.reader(open('data/acris/ACRIS_RemarksRecords.csv'), delimiter='|')
writer = csv.writer(open('data/acris/remarks_records.csv', 'w'))

header = ['Unique_Key','Record_type','Seq','Text']
writer.writerow(header)

for row in reader:
    writer.writerow(row)