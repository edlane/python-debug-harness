#!/usr/bin/python
from __future__ import print_function

__author__ = 'ed'

import sys
import harness

@harness.func_plug
def foo_1(x, y=1, **kwargs):
    return x * y

@harness.func_plug
def foo_2(*args, **kwargs):
    return 2

@harness.func_plug
def bar(a,b,c,d,e):
    return a + b + c + d + e

@harness.func_plug
def add(*args):
    result = 0
    for x in args:
        result = result + x
    return result

@harness.func_plug
def maxit(*args):
    amax = args[0]
    for x in args:
        if x > amax:
            amax = x
    return amax

if __name__ == "__main__":

    harness.replay()

    adict = {'hello': 1, 'world': 2}

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
