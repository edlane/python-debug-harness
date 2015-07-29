#!/usr/bin/python
from __future__ import print_function

__author__ = 'ed lane'

import sys
import jsonpickle

prog_name = __file__.split('/')[-1]


class Harness_globals():
    prog_name = __file__.split('/')[-1]
    harness_file_name = '/tmp/harness.' + prog_name + '.jsonpkl'
    f = open(harness_file_name, 'a+')
    f.seek(0)
    json_string = f.read()
    try:
        json_dict = jsonpickle.loads(json_string)
    except:
        json_dict = {}

    @staticmethod
    def save():
        Harness_globals.f.truncate(0)
        print (jsonpickle.dumps(Harness_globals.json_dict), file=Harness_globals.f)


# text menu for replaying a function using previously saved parameters
def replay():
    func_list = []
    for x in Harness_globals.json_dict:
        func_list.append(x)

    while True:
        print ('c : <continue>')
        print ('q : <quit>')
        print ('--------------')
        n = 0
        for x in func_list:
            print (n, ':', x)
            n += 1

        func_input = raw_input('\nenter function # to replay ===> ')
        if func_input == 'c':
            return
        elif func_input == 'q':
            exit()
        else:
            func_int = int(func_input)
            # print (Harness_globals.json_dict[func_list[func_int]])
            print ('function =', func_list[func_int])
            print ('*args = ')
            for each in Harness_globals.json_dict[func_list[func_int]][0]:
                # print *args
                print (each)
            print ('**kwargs = ')
            for each in sorted(Harness_globals.json_dict[func_list[func_int]][1]):
                # print **kwargs
                print (each, '=', Harness_globals.json_dict[func_list[func_int]][1][each] )

            func_input = raw_input('proceed using these parameters??? (Y/n) (x=delete) ===> ')
            if func_input == '':
                # No input default to a 'Y'
                func_input = 'Y'
            if func_input in 'x':
                del(Harness_globals.json_dict[func_list[func_int]])
                del(func_list[func_int])
                Harness_globals.save()
                continue
            if func_input in 'Yy':
                function = getattr(sys.modules[__name__], func_list[func_int])
                args = Harness_globals.json_dict[func_list[func_int]][0]
                kwargs = Harness_globals.json_dict[func_list[func_int]][1]
                print ('result = ', function(*args, **kwargs), '\n')


# decorator to save/restore function parameters at run-time
# useful for replaying/debugging a function in a symbolic debugger such as Eclipse or Pycharm
def func_plug(func):
    def inner(*args, **kwargs):
        if func.__name__ in Harness_globals.json_dict:
            # this function's params already existed in harness file
            # so return saved params...
            args = Harness_globals.json_dict[func.__name__][0]
            kwargs = Harness_globals.json_dict[func.__name__][1]
            # print ('restoring "[*args, **kwargs]" for ' + func.__name__ + ' = ' + repr([args, kwargs]))
            return func(*args, **kwargs)

        # first time we have seen params for this function...
        # so save params to harness file
        Harness_globals.json_dict[func.__name__] = [args, kwargs]
        print ('saving "[*args, **kwargs]" for ' + func.__name__ + ' = ' + repr([args, kwargs]))
        Harness_globals.save()

        return func(*args, **kwargs)
    return inner


@func_plug
def foo_1(x, y=1, **kwargs):
    return x * y

@func_plug
def foo_2(*args, **kwargs):
    return 2

@func_plug
def bar(a,b,c,d,e):
    return a + b + c + d + e

@func_plug
def add(*args):
    result = 0
    for x in args:
        result = result + x
    return result

@func_plug
def maxit(*args):
    amax = args[0]
    for x in args:
        if x > amax:
            amax = x
    return amax




