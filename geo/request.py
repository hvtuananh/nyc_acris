#!/usr/bin/python

import sys
sys.path.append('../../geoclient')
import pickle
from geoclient import GeoClient
from multiprocessing import Process, Pool
import traceback

geo = GeoClient()

addresses = pickle.load(open('addresses.bin'))

def standardize(address):
    try:
        addr_str = str(address['ACRIS_Addr1']) + ',' + str(address['ACRIS_City']) + ',' + str(address['ACRIS_State']) + ',' + str(address['ACRIS_Zip'])
        address['ACRIS_Hash'] = hash(addr_str)
        results = geo.standardize(addr_str)
        print addr_str
    except:
        traceback.print_exc()
        print "This is exception!" + int(1)
    
    if results is None:
        return None
    else:
        return dict(address.items() + results.items())

pool = Pool(processes=16)
results = pool.map(standardize, addresses.values())

pickle.dump(results, open('geocoded.bin','w'))