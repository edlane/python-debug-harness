from __future__ import print_function
__author__ = 'ed'

import sys
import json

def harness(func):
    def inner(*args, **kwargs): #1
        # print ( "Arguments were: %s, %s, %s" % (func.__name__, args, kwargs))
        f = open('harness.json', 'a+')
        f.seek(0)
        json_string = f.read()
        print (json_string)
        json_dict = {}
        try:
            json_dict = json.loads(json_string)
        except:
            pass
        print (json_dict)

        f.truncate(0)
        json_dict[func.__name__] = [args, kwargs]
        print (json.dumps(json_dict), file=f)
        # print (json.dumps(kwargs), file=f)
        return func(*args, **kwargs) #2
    return inner

@harness
def foo1(x, y=1, **kwargs):
    return x * y

@harness
def foo2(*args, **kwargs):
    return 2

adict = {'hello': 1, 'world': 2}
foo1(5, 4)
foo1(1, z=12)
foo1(1)
foo2(adict, adict,adict, bob=adict)

