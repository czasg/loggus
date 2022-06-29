# coding: utf-8
import time
import loggus

from loggus.hooks import TimedRotatingFileHook


def loop(index):
    time.sleep(0.5)
    loggus.info(index)


if __name__ == '__main__':
    loggus.AddHook(TimedRotatingFileHook("TimedRotatingFileHook.log", when="s", interval=5, backupCount=1))
    for index in range(100):
        loop(index)
