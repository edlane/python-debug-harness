#!/usr/bin/python
from __future__ import print_function

__author__ = 'ed lane'

import sys
import time
# import datetime
from datetime import datetime, date, time
import harness

@harness.decor_plug(harness.FIRST)
def foo_1(x, y=1, **kwargs):
    return x * y

@harness.decor_plug(harness.FIRST)
def foo_2(*args, **kwargs):
    return 2

@harness.decor_plug(harness.FIRST)
def bar(a,b,c,d,e):
    return a + b + c + d + e

@harness.decor_plug(harness.FIRST)
def add(*args):
    result = 0
    for x in args:
        result = result + x
    return result

@harness.decor_plug(harness.FIRST)
def maxit(*args):
    amax = args[0]
    for x in args:
        if x > amax:
            amax = x
    return amax

@harness.decor_plug(harness.FIRST)
def first_time(dt):
    return dt

@harness.decor_plug(harness.LAST)
def last_time(dt):
    return dt


class weird_stuff():

    a = 'string'
    b = 10
    def seta(self, x):
        self.b = x

def main():
    ws = weird_stuff()
    ws.seta(5)

    adict = {'hello': 1, 'world': 2}

    result = foo_2(ws)
    print ('result = ' + str(result))

    result = foo_1(5, 4)
    print ('result = ' + str(result))
    result = foo_1(1, z=12)
    print ('result = ' + str(result))
    result = foo_1(1)
    print ('result = ' + str(result))
    result = foo_2(adict, adict, adict, adict,
                   adict, adict, adict, adict,
                   alice='alice',
                   charles='chuck',
                   bob=adict,)
    print ('result = ' + str(result))
    result = bar(1,2,3,4,5)
    print ('result = ' + str(result))
    result = add(1,2,3,4,5)
    print ('result = ' + str(result))
    result = maxit(10,222,3,43,55)
    print ('result = ' + str(result))
    result = first_time(datetime.now())
    print ('result = ' + str(result))
    result = last_time(datetime.now())
    print ('result = ' + str(result))

    result = harness.multiply(1, 2, 3, 4)
    print ('result = ' + str(result))


if __name__ == "__main__":
    harness.replay()
    main()


