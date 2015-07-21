#!/usr/bin/python
__author__ = 'ed'
import os
import sys
from resource import getrusage as resource_usage, RUSAGE_SELF
from time import time as timestamp

from multiprocessing import Process, Queue, Pipe


def trueit_local():
    return True

def trueit_queue(q):
    q.put(True)

def trueit_pipe(conn):
    conn.send(True)
    conn.close()


if __name__ == '__main__':


    reps = int(sys.argv[1])
    if reps != 0:
        for test in sys.argv[2:]:
            start_time, start_resources = timestamp(), resource_usage(RUSAGE_SELF)
            if test == '1':
                print('os.system(\'true\') =')
                for i in xrange(0, reps):
                    os.system('true')

            elif test == '2':
                print('python local call, \'True\' =')
                for i in xrange(0, reps):
                    trueit_local()

            elif test == '3':
                print('os.system, python executable =')
                for i in xrange(0, reps):
                    command = sys.argv[0] + " 0 2"
                    os.system(command)

            elif test == '4':
                q = Queue()
                print('multiprocess, queue =')
                for i in xrange(0, reps):
                    p = Process(target=trueit_queue, args=(q,))
                    p.start()
                    r = q.get()
                    p.join()

            elif test == '5':
                print('multiprocess, pipe =')
                parent_conn, child_conn = Pipe()
                for i in xrange(0, reps):
                    p = Process(target=trueit_pipe, args=(child_conn,))
                    p.start()
                    r = parent_conn.recv()
                    p.join()

            elif test == '6':
                print('os.system, python executable =')
                for i in xrange(0, reps):
                    command = "/usr/bin/salt-call test.ping"
                    os.system(command)


            end_resources, end_time = resource_usage(RUSAGE_SELF), timestamp()

            results =  {'real': end_time - start_time,
                'sys': end_resources.ru_stime - start_resources.ru_stime,
                'user': end_resources.ru_utime - start_resources.ru_utime}
            print results
            print '=', reps / results['real'], 'calls per second\n'
