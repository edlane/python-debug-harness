from __future__ import print_function

__author__ = 'ed'

import sys
import json

def harness(func):
    def inner(*args, **kwargs):
        f = open('/tmp/harness.json', 'a+')
        f.seek(0)
        json_string = f.read()
        # print (json_string)
        json_dict = {}
        try:
            json_dict = json.loads(json_string)
        except:
            pass

        if func.__name__ in json_dict:
            # this function's params already existed in file
            # so return saved params...
            args = json_dict[func.__name__][0]
            kwargs = json_dict[func.__name__][1]
            return func(*args, **kwargs)

        # first time we have seen params for this function...
        # save params to file
        json_dict[func.__name__] = [args, kwargs]
        f.truncate(0)
        print (json.dumps(json_dict), file=f)
        print ('saving ' + repr(json_dict))

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

if __name__ == '__main__':

    adict = {'hello': 1, 'world': 2}

    result = foo1(5, 4)
    result = foo1(1, z=12)
    result = foo1(1)
    result = foo2(adict, adict, adict, bob=adict)

    result = bar(1,2,3,4,5)

