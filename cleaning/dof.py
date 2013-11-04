#!/usr/bin/python

'''
This script filter all BBL in lot_records before adding it to database
'''

import csv
import pickle

def cut_string(string):
    return string[7:]

files = ['bronx.csv','brooklyn.csv','manhattan.csv','queens.csv','stisland.csv']
writer = csv.writer(open('data/dof/tax.csv', 'w'))
bbls_keep = pickle.load(open('pluto.bin'))

has_header = False
for file in files:
    reader = csv.reader(open('data/dof/' + file))
    header = map(cut_string, reader.next())
    if not has_header:
        has_header = True
        writer.writerow(header)

    for row in reader:
        borough = int(row[header.index('id-boro')])
        block = int(row[header.index('id-block')])
        lot = int(row[header.index('id-lot')])
        bbl = long(borough*1000000000+block*10000+lot)
        if bbl not in bbls_keep:
            continue
        
        writer.writerow(row)