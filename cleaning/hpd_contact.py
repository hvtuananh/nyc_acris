#!/usr/bin/python

'''
This script filter all BBL in lot_records before adding it to database
'''

import csv
import pickle

reader = csv.reader(open('data/hpd/RegistrationContact.csv'))
writer = csv.writer(open('data/hpd/registration_contact.csv', 'w'))
hpd_keep = pickle.load(open('hpd.bin'))

header = reader.next()
writer.writerow(header)

regids = set()

for row in reader:
    regid = long(row[header.index('RegistrationID')])
    if regid not in hpd_keep:
        continue
        
    writer.writerow(row)