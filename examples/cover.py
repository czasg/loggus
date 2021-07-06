# coding: utf-8
import loggus
import time

if __name__ == '__main__':
    entry = loggus.withKwargs(name="CzaOrz")
    for i in range(101):
        loggus.cover(i)
        time.sleep(0.1)
    entry.info("pass")
