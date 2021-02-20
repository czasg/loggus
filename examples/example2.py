import time
import loggus

from loggus.hooks import FileHook, RotatingFileHook, TimedRotatingFileHook


def test():
    for i in range(5):
        loggus.info("hello world")
        loggus.warning("hello world")
        loggus.error("hello world")
        time.sleep(3)


if __name__ == '__main__':
    loggus.CloseColor()
    loggus.AddHook(TimedRotatingFileHook("cza.log", when="s", interval=3))
    test()
