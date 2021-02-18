# coding: utf-8
def IsILevel(level):
    return isinstance(level, Level)


class Level:

    def __init__(self, string: str, integer: int):
        self.string = string
        self.integer = integer

    def __eq__(self, other):
        return self.integer == other.integer

    def __gt__(self, other):
        return self.integer >= other.integer

    def __lt__(self, other):
        return self.integer <= other.integer


DEBUG = Level("debug", 10)
INFO = Level("info", 10)
WARNING = Level("warning", 10)
ERROR = Level("error", 10)
PANIC = Level("panic", 10)
