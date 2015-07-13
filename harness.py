#!/usr/bin/python
from __future__ import print_function

__author__ = 'ed'

import sys
import json


class Harness_globals():
    harness_file = '/tmp/harness.json'
    json_dict = {}


def harness(func):
    def inner(*args, **kwargs):
        f = open(Harness_globals.harness_file, 'a+')
        f.seek(0)
        json_string = f.read()
        try:
            Harness_globals.json_dict = json.loads(json_string)
        except:
            pass

        if func.__name__ in Harness_globals.json_dict:
            # this function's params already existed in harness file
            # so return saved params...
            args = Harness_globals.json_dict[func.__name__][0]
            kwargs = Harness_globals.json_dict[func.__name__][1]
            print ('restoring "[*args, **kwargs]" for ' + func.__name__ + ' = ' + repr([args, kwargs]))
            return func(*args, **kwargs)

        # first time we have seen params for this function...
        # so save params to harness file
        Harness_globals.json_dict[func.__name__] = [args, kwargs]
        f.truncate(0)
        print (json.dumps(Harness_globals.json_dict), file=f)
        print ('saving "[*args, **kwargs]" for ' + func.__name__ + ' = ' + repr([args, kwargs]))

        return func(*args, **kwargs)
    return inner

@harness
def foo_1(x, y=1, **kwargs):
    return x * y

@harness
def foo_2(*args, **kwargs):
    return 2

@harness
def bar(a,b,c,d,e):
    return a + b + c + d + e

@harness
def add(*args):
    result = 0
    for x in args:
        result = result + x
    return result

@harness
def maxit(*args):
    amax = args[0]
    for x in args:
        if x > amax:
            amax = x
    return amax


if __name__ == '__main__':

    adict = {'hello': 1, 'world': 2}

    result = foo_1(5, 4)
    print ('result = ' + str(result))
    result = foo_1(1, z=12)
    print ('result = ' + str(result))
    result = foo_1(1)
    print ('result = ' + str(result))
    result = foo_2(adict, adict, adict, adict,
                   adict, adict, adict, adict,
                   adict, adict, adict, bob=adict)
    print ('result = ' + str(result))
    result = bar(1,2,3,4,5)
    print ('result = ' + str(result))
    result = add(1,2,3,4,5)
    print ('result = ' + str(result))
    result = maxit(10,222,3,43,55)
    print ('result = ' + str(result))

