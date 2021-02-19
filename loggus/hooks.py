# coding: utf-8
import os

from loggus.level import GetAllLevels


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
