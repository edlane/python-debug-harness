#!/usr/bin/python
from __future__ import print_function

__author__ = 'ed lane'

import sys
import jsonpickle
import __main__


FIRST = 0
LAST = 1
ALL = 2

ARGS = 'args'
KWARGS = 'kwargs'
SELF = 'self'
CLASS = 2


class Harness_globals():
    harness_file_name = '/tmp/harness-' + sys.argv[0].rsplit('/', 1)[1].rsplit('.', 1)[0] + '.jsonpkl'
    f = open(harness_file_name, 'a+')
    f.seek(0)
    json_string = f.read()
    json_dict = {}
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
    for x in sorted(Harness_globals.json_dict):
        func_list.append(x)

    while True:
        print ('c : <continue>')
        print ('q : <quit>')
        print ('d : <disable menu>')
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
        elif func_input == 'd':
            Harness_globals.json_dict['__enable_menu__'] = True
            Harness_globals.save()
            return
        else:
            func_int = int(func_input)
            # print (Harness_globals.json_dict[func_list[func_int]])
            print ('function =', func_list[func_int])
            more = len(Harness_globals.json_dict[func_list[func_int]]) > 1
            i = 0
            for every in Harness_globals.json_dict[func_list[func_int]]:
                if more:
                    print ('----------- ', i)
                    i += 1
                print ('*args = ')
                for each in sorted(every[ARGS]):
                    # print *args
                    print (each)
                print ('**kwargs = ')
                for each in sorted(every[KWARGS]):
                    print (each, '=', every[KWARGS][each])

            func_input = raw_input('call function using these parameters??? (Y/n) (x=delete) ===> ')
            if func_input == '':
                # No input default to a 'Y'
                func_input = 'Y'
            if func_input in 'x':
                del(Harness_globals.json_dict[func_list[func_int]])
                del(func_list[func_int])
                Harness_globals.save()
                continue
            if func_input in 'Yy':
                module_name = func_list[func_int].split('.')[0]
                function_name = func_list[func_int].split('.')[1]
                if SELF in Harness_globals.json_dict[func_list[func_int]][FIRST]:
                    # this is an class instance
                    function = Harness_globals.json_dict[func_list[func_int]][FIRST][SELF][2]
                else:
                    # this is a classless "top module" function
                    function = getattr(sys.modules[module_name], function_name)
                args = Harness_globals.json_dict[func_list[func_int]][FIRST][ARGS]
                kwargs = Harness_globals.json_dict[func_list[func_int]][FIRST][KWARGS]
                print ('function = ', func_list[func_int], 'result = ', function(*args, **kwargs), '\n')


# decorator to save/restore function parameters at run-time
# This is useful for capturing function parameters and then later replaying/debugging that function in a
# symbolic debugger such as Eclipse or Pycharm
def decor_record(recall):
    def func_record(func):
        def inner(*args, **kwargs):
            if func.func_code.co_varnames[0] == 'self':
                class_name = args[0].__class__.__name__
                mod_func_name = func.func_globals['__name__'] + '.' + class_name + '.' + func.__name__
            else:
                mod_func_name = func.func_globals['__name__'] + '.' + func.__name__
            if mod_func_name in Harness_globals.json_dict and recall == FIRST:
                # this function's params already existed in harness file
                # so return saved params...
                if func.func_code.co_varnames[0] == 'self':
                    args = args[:1]
                    args += Harness_globals.json_dict[mod_func_name][FIRST][ARGS][1:]
                    # args = Harness_globals.json_dict[mod_func_name][FIRST][ARGS]
                else:
                    args = Harness_globals.json_dict[mod_func_name][FIRST][ARGS]
                kwargs = Harness_globals.json_dict[mod_func_name][FIRST][KWARGS]
                return func(*args, **kwargs)

            # first time we have seen params for this function...
            # OR the decorator specified replacement on every call
            # so save the params to harness file
            if not Harness_globals.json_dict.has_key(mod_func_name) or recall == LAST:
                Harness_globals.json_dict[mod_func_name] = []

            d = {}
            d[ARGS] = args
            d[KWARGS] = kwargs
            Harness_globals.json_dict[mod_func_name].append(d)
            print ('saving... ' + mod_func_name + ' = ' + repr(d))
            Harness_globals.save()
            if func.func_code.co_varnames[0] == 'self':
                Harness_globals.json_dict[mod_func_name][FIRST][SELF] = (args[0], func.func_name, func)

            return func(*args, **kwargs)
        return inner
    return func_record


@decor_record(FIRST)
def multiply(*args):
    result = 1
    for x in args:
        result = result * x
    return result
