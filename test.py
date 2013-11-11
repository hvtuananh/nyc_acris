#!/usr/bin/python

from multiprocessing import Process, Pool, Queue
import time
import random

def f(x):
    print x*x
    time.sleep(random.randint(1, 10))
    return x
    
if __name__ == '__main__':
    pool = Pool(processes=4)
    result = pool.map(f, range(10))
    print result