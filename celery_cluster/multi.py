import os
import threading


def prinfo(args):
    print "pid=", os.getegid(), "arg1=", args[0], ",arg2=", args[1]


class SumThread(threading.Thread):
    def __init__(self, low, high):
        super(SumThread, self).__init__()
        self.low = low
        self.high = high
        self.total = 0

    def run(self):
        for i in range(self.low, self.high):
            self.total += i


class Student(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def print_score(self):
        print '%s:%d' % (self.name, self.score)
