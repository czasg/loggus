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


def SafeRemove(*files):
    for filename in files:
        if os.path.exists(filename):
            os.remove(filename)


def SafeMoveFile(source, destination):
    if not os.path.exists(source):
        return
    SafeRemove(destination)
    os.rename(source, destination)


class IHook:

    def GetLevels(self) -> list:
        raise NotImplementedError

    def Fire(self, entry, level, msg, output) -> None:
        raise NotImplementedError


class FileHook(IHook):
    stream = None

    def __init__(self, filename, mode="a", encoding="utf-8"):
        """
        :param filename: The file path.
        :param mode:
        :param encoding:
        """
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
        """
        :param filename: The file path.
        :param mode:
        :param encoding:
        :param maxBytes: Rollover occurs whenever the current log file is nearly maxBytes in length.
            If maxBytes is zero, rollover never occurs.
        :param backupCount: If backupCount is >= 1, the system will successively create new files
            with the same pathname as the base file, like "log.log"、"log.log.1"、"log.log.2"...
            If backupCount is zero, create new files with the same pathname as the base file always.
        """
        super(RotatingFileHook, self).__init__(filename, mode, encoding)
        self.maxBytes = maxBytes
        self.backupCount = backupCount

    def Fire(self, entry, level, msg, output) -> None:
        if self.NeedRollover(output):
            self.DoRollover()
        self.stream.write(output)
        self.stream.flush()

    def NeedRollover(self, output) -> bool:
        if self.maxBytes <= 0:
            return False
        self.stream.seek(0, 2)
        return (self.stream.tell() + len(output)) >= self.maxBytes

    def DoRollover(self):
        if hasattr(self.stream, "close"):
            self.stream.close()
            self.stream = None
        if self.backupCount < 1:
            SafeRemove(self.filename)
            self.stream = open(self.filename, mode=self.mode, encoding=self.encoding)
            return
        for index in range(self.backupCount - 1, 0, -1):
            SafeMoveFile(f"{self.filename}.{index}", f"{self.filename}.{index + 1}")
        SafeMoveFile(self.filename, f"{self.filename}.1")
        self.stream = open(self.filename, mode=self.mode, encoding=self.encoding)


class TimedRotatingFileHook(RotatingFileHook):

    def __init__(self, filename, when="h", interval=1, mode="a", encoding="utf-8", backupCount=3):
        """
        :param filename: The file path.
        :param when:
            when="s", rollover occurs whenever interval seconds
            when="m", rollover occurs whenever interval minutes
            when="h", rollover occurs whenever interval hours
            when="d", rollover occurs whenever interval days
        :param interval:
        :param mode:
        :param encoding:
        :param backupCount:
        """
        super(TimedRotatingFileHook, self).__init__(filename, mode, encoding, 0, backupCount)
        self.when = when.upper()
        self.backupCount = backupCount
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
        self.interval = self.interval * interval
        if os.path.exists(self.filename):
            current = os.stat(self.filename)[ST_MTIME]
        else:
            current = int(time.time())
        self.nextRolloverAt = self.NextRollover(current)

    def CheckFilesToDelete(self) -> list:
        dirName, baseName = os.path.split(self.filename)
        fileNames = os.listdir(dirName)
        result = []
        prefix = baseName + "."
        plen = len(prefix)
        for fileName in fileNames:
            if fileName[:plen] == prefix:
                suffix = fileName[plen:]
                if self.extMatch.match(suffix):
                    result.append(os.path.join(dirName, fileName))
        if len(result) < self.backupCount:
            result = []
        else:
            result.sort()
            result = result[:len(result) - self.backupCount]
        return result

    def NextRollover(self, current) -> int:
        return current + self.interval

    def NeedRollover(self, output) -> bool:
        return int(time.time()) >= self.nextRolloverAt

    def DoRollover(self):
        if hasattr(self.stream, "close"):
            self.stream.close()
            self.stream = None

        backName = f"{self.filename}.{time.strftime(self.suffix, time.localtime(self.nextRolloverAt))}"
        SafeMoveFile(self.filename, backName)
        SafeRemove(*self.CheckFilesToDelete())
        self.stream = open(self.filename, mode=self.mode, encoding=self.encoding)
        self.nextRolloverAt = self.NextRollover(self.nextRolloverAt)
