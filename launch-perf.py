#!/usr/bin/python
__author__ = 'ed'
import os
import sys
from multiprocessing import Process, Queue, Pipe


def trueit():
    return True

def trueit_queue(q):
    q.put(True)

def trueit_pipe(conn):
    conn.send(True)
    conn.close()


if __name__ == '__main__':

    reps = int(sys.argv[2])
    if sys.argv[1] == '1':
        for i in xrange(1, reps):
            os.system('true')

    elif sys.argv[1] == '2':
        for i in xrange(1, reps):
            trueit()

    elif sys.argv[1] == '3':
        for i in xrange(1, reps):
            command = "./launchit.py 2 1"
            os.system(command)

    elif sys.argv[1] == '4':
        q = Queue()
        for i in xrange(1, reps):
            p = Process(target=trueit_queue, args=(q,))
            p.start()
            r = q.get()
            p.join()

    elif sys.argv[1] == '5':
        parent_conn, child_conn = Pipe()
        for i in xrange(1, reps):
            p = Process(target=trueit_pipe, args=(child_conn,))
            p.start()
            r = parent_conn.recv()
            p.join()