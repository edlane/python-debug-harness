#!/usr/bin/python
from __future__ import print_function

__author__ = 'ed'

import sys
import json
import urwid

json_dict = {}

def harness(func):
    def inner(*args, **kwargs):
        global json_dict
        f = open('/tmp/harness.json', 'a+')
        f.seek(0)
        json_string = f.read()
        # print (json_string)
        # json_dict = {}
        try:
            json_dict = json.loads(json_string)
        except:
            pass

        if func.__name__ in json_dict:
            # this function's params already existed in file
            # so return saved params...
            args = json_dict[func.__name__][0]
            kwargs = json_dict[func.__name__][1]
            print ('restoring "[*args, **kwargs]" for ' + func.__name__ + ' = ' + repr([args, kwargs]))
            return func(*args, **kwargs)

        # first time we have seen params for this function...
        # so save params to a file
        json_dict[func.__name__] = [args, kwargs]
        f.truncate(0)
        print (json.dumps(json_dict), file=f)
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

# def show_or_exit(key):
#     if key in ('q', 'Q'):
#         raise urwid.ExitMainLoop()
#     txt.set_text(repr(key))

# choices = u'Chapman Cleese Gilliam Idle Jones Palin'.split()

def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    for c in choices:
        button = urwid.Button(c)
        urwid.connect_signal(button, 'click', item_chosen, c)
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def item_chosen(button, choice):
    response = urwid.Text([u'You chose ', choice, u'\n'])
    # done = urwid.Button(u'Ok')
    done = urwid.Button(repr(json_dict[choice]))
    urwid.connect_signal(done, 'click', exit_program)
    main.original_widget = urwid.Filler(urwid.Pile([response,
        urwid.AttrMap(done, None, focus_map='reversed')]))

def exit_program(button):
    raise urwid.ExitMainLoop()


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

    choices = json_dict.keys()

    # txt = urwid.Text(u"Hello World")
    # fill = urwid.Filler(txt, 'top')
    # loop = urwid.MainLoop(fill, unhandled_input=show_or_exit)
    # loop.run()

    main = urwid.Padding(menu(u'Function to Replay:', choices), left=2, right=2)
    top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
        align='center', width=('relative', 60),
        valign='middle', height=('relative', 60),
        min_width=20, min_height=9)
    urwid.MainLoop(top, palette=[('reversed', 'standout', '')]).run()
