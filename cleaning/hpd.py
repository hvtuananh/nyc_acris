#!/usr/bin/python

'''
This script filter all BBL in lot_records before adding it to database
'''

import csv
import pickle

reader = csv.reader(open('data/hpd/Registration.csv'))
writer = csv.writer(open('data/hpd/registration.csv', 'w'))
bbls_keep = pickle.load(open('pluto.bin'))

header = reader.next()
writer.writerow(header)

regids = set()

for row in reader:
    bbl = long(row[header.index('bbl')])
    if bbl not in bbls_keep:
        continue
        
    regids.add(int(row[header.index('RegistrationID')]))
        
    writer.writerow(row)
    
pickle.dump(regids, open('hpd.bin', 'w'))