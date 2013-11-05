#!/usr/bin/python

from multiprocessing import Process, Pool
import time

def f(x,y):
    print x*x
    time.sleep(10)
    
if __name__ == '__main__':
    pool = Pool(processes=4)
    result = pool.map(f, [(1,1),(2,2)])