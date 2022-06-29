# coding: utf-8
import loggus

from loggus.hooks import FileHook


def loop(index):
    loggus.info(index)


if __name__ == '__main__':
    loggus.AddHook(FileHook("FileHook.log"))
    for index in range(100):
        loop(index)
