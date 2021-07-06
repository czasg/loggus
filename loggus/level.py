# coding: utf-8
import logging


def IsLevel(level):
    return level in GetAllLevels()


def GetAllLevels():
    return [DEBUG, INFO, WARNING, ERROR, PANIC]


class Level:

    def __init__(self, string: str, integer: int, color: str):
        self.describe = string
        self.value = integer
        self.color = color.format(string)
        self.colorTmp = color

    def toColor(self, msg: str):
        return self.colorTmp.format(msg)

    def __eq__(self, other):
        return self.value == other.value

    def __gt__(self, other):
        return self.value > other.value

    def __ge__(self, other):
        return self.value >= other.value

    def __lt__(self, other):
        return self.value < other.value

    def __le__(self, other):
        return self.value <= other.value

    def __hash__(self):
        return self.value

    def __str__(self):
        return self.describe

    __repr__ = __str__


DEBUG = Level("debug", logging.DEBUG, "\033[1;37m{}\033[0m")
INFO = Level("info", logging.INFO, "\033[1;32m{}\033[0m")
WARNING = Level("warning", logging.WARNING, "\033[1;33m{}\033[0m")
ERROR = Level("error", logging.ERROR, "\033[1;31m{}\033[0m")
PANIC = Level("panic", logging.FATAL, "\033[1;36m{}\033[0m")
RATE = Level("rate", logging.CRITICAL, "\033[1;32m{}\033[0m")
