# coding: utf-8
import os
import re
import time

from loggus.level import GetAllLevels

ST_MODE = 0
ST_INO = 1
ST_DEV = 2
ST_NLINK = 3
ST_UID = 4
ST_GID = 5
ST_SIZE = 6
ST_ATIME = 7
ST_MTIME = 8
ST_CTIME = 9
MIDNIGHT = 24 * 60 * 60


def IsIHook(hook) -> bool:
    return isinstance(hook, IHook)


def SafeMoveFile(source, destination):
    if not os.path.exists(source):
        return
    if os.path.exists(destination):
        os.remove(destination)
    os.rename(source, destination)


class IHook:

    def GetLevels(self) -> list:
        raise NotImplementedError

    def Fire(self, entry, level, msg, output) -> None:
        raise NotImplementedError


class FileHook(IHook):
    stream = None

    def __init__(self, filename, mode="a", encoding="utf-8"):
        self.filename = os.path.abspath(filename)
        self.mode = mode
        self.encoding = encoding
        self.stream = open(filename, mode=mode, encoding=encoding)

    def GetLevels(self):
        return GetAllLevels()

    def Fire(self, entry, level, msg, output) -> None:
        self.stream.write(output)
        self.stream.flush()

    def __del__(self):
        if hasattr(self.stream, "close"):
            self.stream.close()


class RotatingFileHook(FileHook):

    def __init__(self, filename, mode="a", encoding="utf-8", maxBytes=1024 * 64, backupCount=3):
        super(RotatingFileHook, self).__init__(filename, mode, encoding)
        self.maxBytes = maxBytes
        self.backupCount = backupCount

    def Fire(self, entry, level, msg, output) -> None:
        if self.NeedRollover(output):
            self.DoRollover()
        self.stream.write(output)
        self.stream.flush()

    def NeedRollover(self, output) -> bool:
        self.stream.seek(0, 2)
        if self.stream.tell() + len(output) >= self.maxBytes:
            return True
        return False

    def DoRollover(self):
        if hasattr(self.stream, "close"):
            self.stream.close()
            self.stream = None
        for index in range(self.backupCount - 1, 0, -1):
            SafeMoveFile(f"{self.filename}.{index}", f"{self.filename}.{index + 1}")
        SafeMoveFile(self.filename, f"{self.filename}.1")
        self.stream = open(self.filename, mode=self.mode, encoding=self.encoding)


class TimedRotatingFileHook(RotatingFileHook):

    def __init__(self, filename, when="h", interval=1, mode="a", encoding="utf-8", maxBytes=1024 * 64, backupCount=3):
        super(TimedRotatingFileHook, self).__init__(filename, mode, encoding, maxBytes, backupCount)
        self.when = when.upper()
        self.interval = interval

        if self.when == 'S':
            self.interval = 1  # one second
            self.suffix = "%Y-%m-%d_%H-%M-%S"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}(\.\w+)?$"
        elif self.when == 'M':
            self.interval = 60  # one minute
            self.suffix = "%Y-%m-%d_%H-%M"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}(\.\w+)?$"
        elif self.when == 'H':
            self.interval = 60 * 60  # one hour
            self.suffix = "%Y-%m-%d_%H"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}_\d{2}(\.\w+)?$"
        elif self.when == 'D' or self.when == 'MIDNIGHT':
            self.interval = 60 * 60 * 24  # one day
            self.suffix = "%Y-%m-%d"
            self.extMatch = r"^\d{4}-\d{2}-\d{2}(\.\w+)?$"
        else:
            raise ValueError("Invalid rollover interval specified: %s" % self.when)
        self.extMatch = re.compile(self.extMatch, re.ASCII)
        self.interval = self.interval * interval  # multiply by units requested
        if os.path.exists(self.filename):
            current = os.stat(self.filename)[ST_MTIME]
        else:
            current = int(time.time())
        self.nextRolloverAt = self.NextRollover(current)

    def NextRollover(self, current):
        return current + self.interval

    def NeedRollover(self, output) -> bool:
        if int(time.time()) >= self.nextRolloverAt:
            return True
        return False

    def DoRollover(self):
        if hasattr(self.stream, "close"):
            self.stream.close()
            self.stream = None

        nextRolloverAt = self.nextRolloverAt

        for index in range(self.backupCount - 1, 0, -1):
            previousFileName = f"{self.filename}.{time.strftime(self.suffix, time.localtime(nextRolloverAt - self.interval * index))}"
            nextFileName = f"{self.filename}.{time.strftime(self.suffix, time.localtime(nextRolloverAt - self.interval * (index - 1)))}"
            SafeMoveFile(previousFileName, nextFileName)
            nextRolloverAt -= self.interval
        SafeMoveFile(self.filename, f"{self.filename}.{time.strftime(self.suffix, time.localtime(nextRolloverAt))}")
        self.stream = open(self.filename, mode=self.mode, encoding=self.encoding)
        self.nextRolloverAt = self.NextRollover(self.nextRolloverAt)
