#!/usr/bin/python

from building import Building
from bbl import BBL
import pickle
import sys

buildings = pickle.load(open('buildings-3430.bin'))
print buildings[BBL(3,3430,41)]