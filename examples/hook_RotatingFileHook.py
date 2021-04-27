# coding: utf-8
import loggus

from loggus.hooks import RotatingFileHook


def loop(index):
    loggus.info(index)


if __name__ == '__main__':
    loggus.AddHook(RotatingFileHook("RotatingFileHook.log", maxBytes=1024, backupCount=3))
    for index in range(100):
        loop(index)
