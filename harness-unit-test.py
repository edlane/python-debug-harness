#!/usr/bin/python
from __future__ import print_function

__author__ = 'ed lane'

import sys
import time
# import datetime
from datetime import datetime, date, time
import harness


class AClass():
    a = 4
    b = 5
    c = 6
    @harness.decor_record(harness.FIRST)
    def hello(self, name):
        print ('hello, ', name)
        # self.b = 12
        return (self.a, self.b, self.c)


@harness.decor_record(harness.FIRST)
def foo_1(x, y=1, **kwargs):
    return x * y

@harness.decor_record(harness.FIRST)
def foo_2(*args, **kwargs):
    return 2

@harness.decor_record(harness.FIRST)
def bar(a,b,c,d,e):
    return a + b + c + d + e

@harness.decor_record(harness.FIRST)
def add(*args):
    result = 0
    for x in args:
        result = result + x
    return result

@harness.decor_record(harness.FIRST)
def maxit(*args):
    amax = args[0]
    for x in args:
        if x > amax:
            amax = x
    return amax

@harness.decor_record(harness.FIRST)
def first_time(dt):
    return dt

@harness.decor_record(harness.ALL)
def every_time(dt):
    return dt

@harness.decor_record(harness.LAST)
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

    aclass = AClass()
    aclass.hello('world')

    adict = {'hello': 1, 'world': 2}

    result = foo_2(ws)
    print ('foo_2 result = ' + str(result))

    result = foo_1(5, 4)
    print ('foo_1 result = ' + str(result))
    result = foo_1(1, z=12)
    print ('foo_1 result = ' + str(result))
    result = foo_1(1)
    print ('foo_1 result = ' + str(result))
    result = foo_2(adict, adict, adict, adict,
                   adict, adict, adict, adict,
                   alice='alice',
                   charles='chuck',
                   bob=adict,)
    print ('foo_2 result = ' + str(result))
    result = bar(1,2,3,4,5)
    print ('bar result = ' + str(result))
    result = add(1,2,3,4,5)
    print ('add result = ' + str(result))
    result = maxit(10,222,3,43,55)
    print ('maxit result = ' + str(result))
    result = first_time(datetime.now())
    print ('first_time result = ' + str(result))
    result = last_time(datetime.now())
    print ('last_time result = ' + str(result))
    result = every_time(datetime.now())
    print ('every_time result = ' + str(result))

    result = harness.multiply(1, 2, 3, 4)
    print ('harness.multiply result = ' + str(result))


if __name__ == "__main__":
    while True:
        harness.replay()
        main()


